from app.models.notification import ActiveScheme, UserAlert
from app import db
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_expiring_schemes(app):
    """
    Background job to scan for expiring documents or schemes.
    Runs inside the Flask application context.
    """
    with app.app_context():
        logger.info("Running automated scan for expiring schemes and documents...")
        
        # Look for schemes expiring in the next 30 days
        expiry_threshold = datetime.utcnow() + timedelta(days=30)
        
        # Query active schemes that have an expiry date and are expiring soon
        expiring_schemes = ActiveScheme.query.filter(
            ActiveScheme.expiry_date != None,
            ActiveScheme.expiry_date <= expiry_threshold,
            ActiveScheme.status == 'active'
        ).all()
        
        alerts_generated = 0
        
        for scheme in expiring_schemes:
            # Check if an alert already exists for this scheme and user recently (basic deduplication)
            existing_alert = UserAlert.query.filter_by(
                user_id=scheme.user_id,
                alert_type="expiry"
            ).filter(
                UserAlert.title.contains(scheme.scheme_name)
            ).first()
            
            if not existing_alert:
                days_left = (scheme.expiry_date - datetime.utcnow()).days
                
                new_alert = UserAlert(
                    user_id=scheme.user_id,
                    alert_type="expiry",
                    title=f"Document Expiry Warning: {scheme.scheme_name}",
                    message=f"Your registration for {scheme.scheme_name} will expire in {days_left} days. Tap the mic and say 'I want to renew {scheme.scheme_name}' for voice guidance.",
                    is_read=False
                )
                db.session.add(new_alert)
                alerts_generated += 1
                
        if alerts_generated > 0:
            db.session.commit()
            logger.info(f"Generated {alerts_generated} new expiry alerts.")
        else:
            logger.info("Scan complete. No new alerts generated.")
