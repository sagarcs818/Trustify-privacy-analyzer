# analyzer/views.py

import json
import requests
from email.utils import parsedate_to_datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

# Import our custom modules
from .policy_sources import APP_PRIVACY_URLS, APP_NAME_ALIASES
from .utils import fetch_privacy_policy
from .models import PrivacyAnalysis

# Import the engine and rename it locally so it doesn't conflict with the view name
from .analysis_engine import analyze_policy as run_analysis_engine 

from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

# ---------------------------
# PAGE VIEWS
# ---------------------------

def home(request):
    """
    Passes the top 5 most searched apps to the homepage to display a 'Trending' section.
    """
    try:
        # Get top 5 most analyzed apps (excluding manual pastes)
        trending_apps = list(
            PrivacyAnalysis.objects.exclude(source="Pasted Policy")
            .values('source')
            .annotate(search_count=Count('source'))
            .order_by('-search_count')[:5]
        )
    except Exception as e:
        print(f"[DB Warning] Could not fetch trending apps: {e}")
        trending_apps = []

    return render(request, 'index.html', {'trending_apps': trending_apps})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Format the email content
        email_body = f"""
        New Contact Form Submission from Trustify:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        try:
            # Send the email
            send_mail(
                subject=f"Trustify Inquiry: {subject}",
                message=email_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER], 
                fail_silently=False,
            )
            
            # This sends the beautiful UI success message to your HTML template
            messages.success(request, 'Thank you! Your message has been sent and we will respond within 24 hours.')
            
            # Redirect back to the contact page to clear the form properly
            return redirect('/contact/') 
            
        except Exception as e:
            print(f"Email sending failed: {e}") 
            
            # This sends a red error UI message if it fails
            messages.error(request, 'Oops! Something went wrong while sending your email. Please try again later.')
            return redirect('/contact/')
            
    return render(request, 'contact.html')



def privacy_analyzer(request):
    return render(request, 'privacy.html')

def team(request):
    return render(request, 'team.html')

def terms_service(request):
    return render(request, 'terms_service.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

# ---------------------------
# API: ANALYZE PASTED POLICY
# ---------------------------

@csrf_exempt
def analyze_policy(request):
    """
    API Endpoint: Handles manually pasted text when an app is missing or blocked.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        text = data.get("policy", "").strip()

        if not text:
            return JsonResponse({"error": "No policy text provided"}, status=400)

        # 1. Run the text through our centralized AI/Keyword engine
        results = run_analysis_engine(text)

        # 2. Try to save the analysis to the Database!
        try:
            PrivacyAnalysis.objects.create(
                source="Pasted Policy",
                policy_text=text,
                is_manual_paste=True,
                safety_score=results["safety_score"],
                consent_risk_score=results["consent_risk_score"],
                sentiment_score=results["sentiment"],
                detected_categories=results["categories"]
            )
        except Exception as db_err:
            print(f"[DB Warning] Could not save manual paste to DB (Migrations run?): {db_err}")

        # 3. Return the results to the frontend
        return JsonResponse({
            "safety_score": results["safety_score"],
            "consent_risk_score": results["consent_risk_score"],
            "categories": results["categories"]
        })

    except Exception as e:
        print(f"[Error in analyze_policy] {e}")
        return JsonResponse({"error": str(e)}, status=500)


# ---------------------------
# API: FIND & ANALYZE APP
# ---------------------------

@csrf_exempt
def find_and_analyze_app(request):
    """
    API Endpoint: Looks up the app, fetches the policy via Playwright, and analyzes it.
    Now includes Smart Caching with HTTP HEAD validation to ensure perfect accuracy!
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        app_name_input = data.get("app", "").strip().lower()

        # Normalize aliases to lowercase
        alias_lookup = {k.lower(): v.lower() for k, v in APP_NAME_ALIASES.items()}
        normalized_urls = {k.lower(): v for k, v in APP_PRIVACY_URLS.items()}

        # Resolve alias (e.g. "fb" -> "facebook")
        alias_name = alias_lookup.get(app_name_input, app_name_input)

        # Grab the URL first so we can ping it for the Last-Modified date
        url = normalized_urls.get(alias_name)

        if not url:
            return JsonResponse({
                "found": False,
                "message": f"Privacy policy for '{app_name_input.title()}' not found. Please paste it manually."
            })

        # 🚀 OPTION 3: SMART HTTP HEADER CHECK & CACHING
        try:
            thirty_days_ago = timezone.now() - timedelta(days=30)
            cached_analysis = PrivacyAnalysis.objects.filter(
                source=alias_name.title(),
                is_manual_paste=False,
                created_at__gte=thirty_days_ago
            ).order_by('-created_at').first()

            if cached_analysis:
                # We have a cache! Let's ping the website to see if it changed recently
                try:
                    # Send a quick HEAD request (takes milliseconds)
                    head_response = requests.head(url, timeout=3, allow_redirects=True)
                    last_modified_header = head_response.headers.get('Last-Modified')
                    
                    if last_modified_header:
                        last_modified_date = parsedate_to_datetime(last_modified_header)
                        
                        # If the website was updated AFTER our database record was created
                        if last_modified_date > cached_analysis.created_at:
                            print(f"[Cache Invalidated] {alias_name.title()} updated their policy! Forcing fresh scrape.")
                            cached_analysis = None # Delete the cached reference to force a new scrape
                        else:
                            print(f"[Cache Verified] {alias_name.title()} policy hasn't changed. Using fast cache.")
                    else:
                        print(f"[Cache Fallback] {alias_name.title()} server hides timestamps. Using 30-day cache.")
                
                except Exception as ping_err:
                    print(f"[HTTP Ping Warning] Could not check date, falling back to cache: {ping_err}")

                # If the cache survived the validation check, return it instantly!
                if cached_analysis:
                    return JsonResponse({
                        "found": True,
                        "app": cached_analysis.source,
                        "safety_score": cached_analysis.safety_score,
                        "safety_out_of": 5,  
                        "consent_risk_score": cached_analysis.consent_risk_score,
                        "categories": cached_analysis.detected_categories,
                        "policy_snippet": cached_analysis.policy_text[:500] + "...",
                        "cached": True
                    })
        except Exception as cache_err:
            print(f"[Cache Warning] Failed to read cache: {cache_err}")

        # If no valid cache exists, fetch the policy using our upgraded Playwright utility
        policy_text = fetch_privacy_policy(url)

        if not policy_text:
            return JsonResponse({
                "found": False,
                "message": f"Privacy policy for '{alias_name.title()}' exists, "
                           "but cannot be retrieved automatically due to regional restrictions "
                           "or website protection. Please paste it manually."
            })

        # 1. Policy fetched successfully -> Run it through the engine
        results = run_analysis_engine(policy_text)

        # 2. Try to save the automatic analysis to the Database!
        try:
            PrivacyAnalysis.objects.create(
                source=alias_name.title(),
                policy_text=policy_text,
                is_manual_paste=False,
                safety_score=results["safety_score"],
                consent_risk_score=results["consent_risk_score"],
                sentiment_score=results["sentiment"],
                detected_categories=results["categories"]
            )
        except Exception as db_err:
            print(f"[DB Warning] Could not save {alias_name} to DB (Migrations run?): {db_err}")

        # 3. Return the results to the frontend dashboard
        return JsonResponse({
            "found": True,
            "app": alias_name.title(),
            "safety_score": results["safety_score"],
            "safety_out_of": 5,  
            "consent_risk_score": results["consent_risk_score"],
            "categories": results["categories"],
            "policy_snippet": policy_text[:500] + "..."
        })

    except Exception as e:
        print(f"[Error in find_and_analyze_app] {e}")
        return JsonResponse({"error": str(e)}, status=500)