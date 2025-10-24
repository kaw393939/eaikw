/**
 * Enhanced Google Analytics 4 Tracking
 * Tracks lead scoring, conversions, and sales funnel progression
 */

// Lead scoring system
window.LeadScoring = {
  score: 0,
  
  addPoints: function(points, reason) {
    this.score += points;
    console.log(`Lead score: +${points} for ${reason}. Total: ${this.score}`);
    
    // Send updated score to GA4
    gtag('event', 'lead_score_update', {
      event_category: 'Lead_Scoring',
      event_label: reason,
      value: points,
      lead_score: this.score
    });
    
    // Trigger qualification events
    if (this.score >= 50 && this.score < 100) {
      gtag('event', 'lead_qualified', {
        event_category: 'Lead_Scoring',
        event_label: 'qualified_lead',
        value: this.score,
        visitor_type: 'qualified'
      });
    } else if (this.score >= 100) {
      gtag('event', 'lead_hot', {
        event_category: 'Lead_Scoring',
        event_label: 'hot_lead',
        value: this.score,
        visitor_type: 'hot_lead'
      });
    }
  }
};

// Enhanced CTA tracking
document.addEventListener('DOMContentLoaded', function() {
  
  // Track all external links
  document.querySelectorAll('a[href^="http"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      const url = this.href;
      let platform = 'external';
      let value = 1;
      
      if (url.includes('linkedin.com')) {
        platform = 'linkedin';
        value = 25; // High-value social platform
        LeadScoring.addPoints(25, 'linkedin_click');
      } else if (url.includes('github.com')) {
        platform = 'github';
        value = 15; // Technical interest
        LeadScoring.addPoints(15, 'github_click');
      } else if (url.includes('discord.gg') || url.includes('discord.com')) {
        platform = 'discord';
        value = 30; // Community engagement
        LeadScoring.addPoints(30, 'discord_click');
      } else if (url.includes('youtube.com')) {
        platform = 'youtube';
        value = 10; // Content engagement
        LeadScoring.addPoints(10, 'youtube_click');
      }
      
      gtag('event', 'click', {
        event_category: 'Outbound_Link',
        event_label: platform,
        value: value,
        funnel_stage: 'interest'
      });
    });
  });
  
  // Track email clicks as high-intent conversions
  document.querySelectorAll('a[href^="mailto:"]').forEach(function(link) {
    link.addEventListener('click', function() {
      LeadScoring.addPoints(50, 'email_click');
      
      // Track as conversion event
      gtag('event', 'conversion', {
        event_category: 'Contact',
        event_label: 'email_click',
        value: 1000, // Estimated lead value
        funnel_stage: 'action'
      });
      
      // Enhanced e-commerce tracking for lead
      gtag('event', 'purchase', {
        transaction_id: 'lead_' + Date.now(),
        value: 1000,
        currency: 'USD',
        items: [{
          item_id: 'email_inquiry',
          item_name: 'Email Contact Lead',
          category: 'Lead_Generation',
          quantity: 1,
          price: 1000
        }]
      });
    });
  });
  
  // Track logo/brand clicks (brand awareness)
  document.querySelectorAll('.logo, .footer-brand').forEach(function(element) {
    element.addEventListener('click', function() {
      gtag('event', 'click', {
        event_category: 'Brand',
        event_label: 'logo_click',
        value: 1
      });
    });
  });
  
  // Track navigation menu usage
  document.querySelectorAll('.nav-links a:not(.cta-button)').forEach(function(link) {
    link.addEventListener('click', function() {
      LeadScoring.addPoints(5, 'navigation_click');
      
      gtag('event', 'click', {
        event_category: 'Navigation',
        event_label: this.textContent.trim().toLowerCase(),
        value: 5,
        funnel_stage: 'awareness'
      });
    });
  });
  
  // Track CTA button clicks with enhanced scoring
  document.querySelectorAll('.cta-button, .btn-primary').forEach(function(button) {
    button.addEventListener('click', function() {
      LeadScoring.addPoints(25, 'cta_click');
      
      gtag('event', 'click', {
        event_category: 'CTA',
        event_label: this.textContent.trim().toLowerCase(),
        value: 25,
        funnel_stage: 'consideration'
      });
    });
  });
  
  // Track about page engagement (credential validation)
  if (window.location.pathname.includes('/about')) {
    LeadScoring.addPoints(15, 'about_page_visit');
    
    gtag('event', 'page_view', {
      event_category: 'Content',
      event_label: 'about_page',
      value: 15,
      funnel_stage: 'consideration'
    });
  }
  
  // Track contact page visits (high intent)
  if (window.location.pathname.includes('/contact') || window.location.hash === '#contact') {
    LeadScoring.addPoints(30, 'contact_page_visit');
    
    gtag('event', 'page_view', {
      event_category: 'Content', 
      event_label: 'contact_section',
      value: 30,
      funnel_stage: 'intent'
    });
  }
  
  // Track repeat visitors (loyalty scoring)
  const visits = localStorage.getItem('visit_count') || 0;
  const newVisitCount = parseInt(visits) + 1;
  localStorage.setItem('visit_count', newVisitCount);
  
  if (newVisitCount > 1) {
    LeadScoring.addPoints(newVisitCount * 5, 'repeat_visitor');
    
    gtag('event', 'repeat_visit', {
      event_category: 'Loyalty',
      event_label: `visit_${newVisitCount}`,
      value: newVisitCount,
      visitor_type: newVisitCount > 3 ? 'loyal' : 'returning'
    });
  }
  
  // Track referrer sources for attribution
  const referrer = document.referrer;
  if (referrer) {
    let source = 'direct';
    if (referrer.includes('linkedin.com')) source = 'linkedin';
    else if (referrer.includes('google.com')) source = 'google';
    else if (referrer.includes('youtube.com')) source = 'youtube';
    else if (referrer.includes('discord.com')) source = 'discord';
    
    gtag('event', 'referral_visit', {
      event_category: 'Attribution',
      event_label: source,
      value: 1
    });
  }
});

// Track form interactions (if contact forms are added later)
function trackFormInteraction(formElement, eventType) {
  const formName = formElement.id || formElement.className || 'unnamed_form';
  
  switch(eventType) {
    case 'start':
      LeadScoring.addPoints(40, 'form_start');
      gtag('event', 'form_start', {
        event_category: 'Form',
        event_label: formName,
        value: 40,
        funnel_stage: 'intent'
      });
      break;
      
    case 'submit':
      LeadScoring.addPoints(100, 'form_submit');
      
      // Major conversion event
      gtag('event', 'conversion', {
        event_category: 'Form',
        event_label: formName + '_submit',
        value: 2000,
        funnel_stage: 'action'
      });
      
      // Enhanced e-commerce conversion
      gtag('event', 'purchase', {
        transaction_id: 'conversion_' + Date.now(),
        value: 2000,
        currency: 'USD',
        items: [{
          item_id: 'contact_form',
          item_name: 'Contact Form Submission',
          category: 'Lead_Generation',
          quantity: 1,
          price: 2000
        }]
      });
      break;
  }
}

// Export for global use
window.trackFormInteraction = trackFormInteraction;

// Debug mode (remove in production)
if (window.location.hostname === 'localhost') {
  console.log('GA4 Enhanced tracking loaded - Debug mode');
  window.LeadScoring.debug = true;
}