# analyzer/models.py
from django.db import models

class PrivacyAnalysis(models.Model):
    # Core Information
    source = models.CharField(max_length=255, help_text="Name of the App or 'Pasted Policy'")  
    policy_text = models.TextField(help_text="The full text of the privacy policy analyzed")
    is_manual_paste = models.BooleanField(default=False, help_text="True if the user pasted the text manually")

    # Analysis Scores
    safety_score = models.FloatField(default=0.0, help_text="Calculated safety rating (1.0 to 5.0 stars)")
    consent_risk_score = models.IntegerField(default=0, help_text="Calculated risk score (0 to 100)")
    sentiment_score = models.FloatField(default=0.0, help_text="NLP sentiment polarity (-1.0 to 1.0)")

    # Extracted Data
    detected_categories = models.JSONField(default=dict, help_text="Dictionary of detected risk categories")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Newest analyses appear first in the admin panel
        verbose_name = "Privacy Analysis"
        verbose_name_plural = "Privacy Analyses"

    def __str__(self):
        return f"{self.source} | Safety: {self.safety_score}⭐ | Risk: {self.consent_risk_score}/100"