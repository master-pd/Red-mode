# file: recovery/support_contact.py
import json
from datetime import datetime

class FacebookSupportContact:
    """ফেসবুক সাপোর্ট কন্টাক্ট"""
    
    def __init__(self):
        self.name = "Facebook Support Contact"
        
    def execute(self, support_request):
        """সাপোর্ট কন্টাক্ট ইনফো"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            support_info = {
                'official_channels': self.get_official_channels(),
                'contact_methods': self.get_contact_methods(),
                'support_categories': self.get_support_categories(),
                'response_times': self.get_response_times(),
                'preparing_for_support': self.get_preparation_guide(),
                'success_tips': self.get_success_tips()
            }
            
            results['data'] = support_info
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def get_official_channels(self):
        """অফিশিয়াল চ্যানেলস"""
        channels = {
            'primary_support': [
                {
                    'name': 'Facebook Help Center',
                    'url': 'https://www.facebook.com/help/',
                    'availability': '24/7',
                    'best_for': 'General issues, account recovery, reporting problems'
                },
                {
                    'name': 'Report a Problem',
                    'url': 'https://www.facebook.com/help/contact/',
                    'availability': '24/7',
                    'best_for': 'Technical issues, bug reports, feature requests'
                },
                {
                    'name': 'Security Help',
                    'url': 'https://www.facebook.com/help/security',
                    'availability': '24/7',
                    'best_for': 'Hacked accounts, privacy concerns, security issues'
                }
            ],
            'specialized_support': [
                {
                    'name': 'Business Support',
                    'url': 'https://www.facebook.com/business/help',
                    'availability': 'Business hours',
                    'best_for': 'Page management, ads, business tools'
                },
                {
                    'name': 'Developer Support',
                    'url': 'https://developers.facebook.com/support/',
                    'availability': 'Business hours',
                    'best_for': 'API issues, app development, platform questions'
                },
                {
                    'name': 'Legal & Copyright',
                    'url': 'https://www.facebook.com/help/contact/169486816475808',
                    'availability': 'Business hours',
                    'best_for': 'Copyright infringement, legal issues, trademark'
                }
            ],
            'community_support': [
                {
                    'name': 'Facebook Community Help',
                    'url': 'https://www.facebook.com/community',
                    'availability': '24/7',
                    'best_for': 'Peer advice, common questions, user experiences'
                },
                {
                    'name': 'Help Community Forum',
                    'url': 'https://www.facebook.com/help/community/',
                    'availability': '24/7',
                    'best_for': 'Discussion, troubleshooting with other users'
                }
            ]
        }
        
        return channels
    
    def get_contact_methods(self):
        """কন্টাক্ট মেথডস"""
        methods = {
            'online_forms': [
                {
                    'form': 'Hacked Account',
                    'url': 'https://www.facebook.com/hacked',
                    'response_time': '24-48 hours',
                    'information_needed': [
                        'Email/phone associated with account',
                        'Approximate date of hacking',
                        'Any accessible recovery options'
                    ]
                },
                {
                    'form': 'Disabled Account',
                    'url': 'https://www.facebook.com/help/contact/260749603972907',
                    'response_time': '48-72 hours',
                    'information_needed': [
                        'Full name on account',
                        'Email/phone used',
                        'ID for verification'
                    ]
                },
                {
                    'form': 'Memorialized Account',
                    'url': 'https://www.facebook.com/help/contact/305593649477238',
                    'response_time': '1-2 weeks',
                    'information_needed': [
                        'Proof of death',
                        'Relationship to deceased',
                        'Account information'
                    ]
                }
            ],
            'email_contacts': [
                {
                    'purpose': 'Legal Inquiries',
                    'email': 'legal@fb.com',
                    'response_time': '3-5 business days',
                    'appropriate_for': 'Legal matters, law enforcement, government'
                },
                {
                    'purpose': 'Press/Media',
                    'email': 'press@fb.com',
                    'response_time': '2-3 business days',
                    'appropriate_for': 'Media inquiries, press releases, interviews'
                },
                {
                    'purpose': 'Data Protection',
                    'email': 'datarequests@fb.com',
                    'response_time': '1 month',
                    'appropriate_for': 'GDPR requests, data access, privacy'
                }
            ],
            'no_contact_methods': [
                'No phone support for personal accounts',
                'No live chat for personal accounts',
                'No office visits for personal support',
                'No social media DMs for support'
            ]
        }
        
        return methods
    
    def get_support_categories(self):
        """সাপোর্ট ক্যাটেগরিস"""
        categories = {
            'account_issues': [
                {
                    'issue': 'Cannot Login',
                    'priority': 'High',
                    'contact_method': 'Help Center > Login Issues',
                    'expected_resolution': '24-72 hours'
                },
                {
                    'issue': 'Hacked Account',
                    'priority': 'High',
                    'contact_method': 'facebook.com/hacked',
                    'expected_resolution': '24-48 hours'
                },
                {
                    'issue': 'Disabled Account',
                    'priority': 'Medium',
                    'contact_method': 'Appeal Form',
                    'expected_resolution': '3-7 days'
                },
                {
                    'issue': 'Memorialized Account',
                    'priority': 'Low',
                    'contact_method': 'Special Form',
                    'expected_resolution': '1-2 weeks'
                }
            ],
            'content_issues': [
                {
                    'issue': 'Removed Content',
                    'priority': 'Medium',
                    'contact_method': 'Appeal through Notification',
                    'expected_resolution': '1-3 days'
                },
                {
                    'issue': 'Copyright Infringement',
                    'priority': 'High',
                    'contact_method': 'Copyright Report Form',
                    'expected_resolution': '24-48 hours'
                },
                {
                    'issue': 'Bullying/Harassment',
                    'priority': 'High',
                    'contact_method': 'Report on Content',
                    'expected_resolution': '24 hours'
                },
                {
                    'issue': 'False Information',
                    'priority': 'Medium',
                    'contact_method': 'Fact-Checking Report',
                    'expected_resolution': '2-3 days'
                }
            ],
            'technical_issues': [
                {
                    'issue': 'App Not Working',
                    'priority': 'Medium',
                    'contact_method': 'Report a Problem',
                    'expected_resolution': '3-5 days'
                },
                {
                    'issue': 'Website Errors',
                    'priority': 'Medium',
                    'contact_method': 'Help Center > Technical Issues',
                    'expected_resolution': '2-4 days'
                },
                {
                    'issue': 'Feature Not Available',
                    'priority': 'Low',
                    'contact_method': 'Help Community',
                    'expected_resolution': 'Varies'
                },
                {
                    'issue': 'Payment Problems',
                    'priority': 'High',
                    'contact_method': 'Payment Support',
                    'expected_resolution': '24-48 hours'
                }
            ]
        }
        
        return categories
    
    def get_response_times(self):
        """রেসপন্স টাইমস"""
        response_times = {
            'immediate_issues': [
                {
                    'issue_type': 'Active Security Threat',
                    'response_time': '1-4 hours',
                    'escalation_path': 'Multiple reports, law enforcement contact'
                },
                {
                    'issue_type': 'Suicide/Self-Harm Reports',
                    'response_time': 'Under 1 hour',
                    'escalation_path': 'Emergency services contact'
                },
                {
                    'issue_type': 'Child Exploitation',
                    'response_time': 'Under 1 hour',
                    'escalation_path': 'NCMEC, law enforcement'
                }
            ],
            'urgent_issues': [
                {
                    'issue_type': 'Hacked Account',
                    'response_time': '24-48 hours',
                    'factors_affecting': 'Time of report, information provided'
                },
                {
                    'issue_type': 'Unauthorized Access',
                    'response_time': '24-48 hours',
                    'factors_affecting': 'Evidence provided, account activity'
                }
            ],
            'standard_issues': [
                {
                    'issue_type': 'Account Recovery',
                    'response_time': '48-72 hours',
                    'factors_affecting': 'Verification complexity, volume'
                },
                {
                    'issue_type': 'Content Appeals',
                    'response_time': '1-3 days',
                    'factors_affecting': 'Content type, policy clarity'
                },
                {
                    'issue_type': 'Technical Issues',
                    'response_time': '3-5 days',
                    'factors_affecting': 'Issue complexity, reproducibility'
                }
            ],
            'factors_affecting_response': [
                'Time of submission (business hours faster)',
                'Completeness of information provided',
                'Issue complexity and priority',
                'Current support volume',
                'Accuracy of contact information'
            ]
        }
        
        return response_times
    
    def get_preparation_guide(self):
        """প্রিপারেশন গাইড"""
        preparation = {
            'before_contacting': [
                {
                    'step': 'Gather Information',
                    'details': 'Collect all relevant account information',
                    'checklist': [
                        'Email/phone associated with account',
                        'Approximate account creation date',
                        'Friends who can vouch for you',
                        'Previous passwords (if remembered)',
                        'Screenshots of error messages'
                    ]
                },
                {
                    'step': 'Try Self-Help',
                    'details': 'Attempt to resolve using available resources',
                    'checklist': [
                        'Check Help Center articles',
                        'Use automated recovery tools',
                        'Search community forums',
                        'Try different browsers/devices',
                        'Clear cache and cookies'
                    ]
                },
                {
                    'step': 'Document Everything',
                    'details': 'Keep records of your issue and attempts',
                    'checklist': [
                        'Dates and times of issues',
                        'Error messages received',
                        'Steps already attempted',
                        'Reference numbers from previous contacts',
                        'Screenshots as evidence'
                    ]
                }
            ],
            'what_to_provide': [
                {
                    'category': 'Account Information',
                    'required': [
                        'Full name on account',
                        'Email/phone used',
                        'Date of birth',
                        'Location when created'
                    ],
                    'helpful': [
                        'Friends list samples',
                        'Previous profile pictures',
                        'Groups you joined',
                        'Recent posts/comments'
                    ]
                },
                {
                    'category': 'Issue Details',
                    'required': [
                        'When the issue started',
                        'What you were doing',
                        'Error messages received',
                        'Steps to reproduce'
                    ],
                    'helpful': [
                        'Screenshots/videos',
                        'Browser/device info',
                        'Network information',
                        'Time zone'
                    ]
                },
                {
                    'category': 'Contact Information',
                    'required': [
                        'Current email for response',
                        'Backup contact method',
                        'Preferred language',
                        'Time zone'
                    ],
                    'helpful': [
                        'Alternative emails',
                        'Phone number',
                        'Best time to contact',
                        'Communication preferences'
                    ]
                }
            ],
            'what_not_to_do': [
                'Do not create multiple accounts to contact support',
                'Do not spam support channels',
                'Do not provide false information',
                'Do not share others\' personal information',
                'Do not use abusive language',
                'Do not threaten legal action immediately'
            ]
        }
        
        return preparation
    
    def get_success_tips(self):
        """সাকসেস টিপস"""
        tips = {
            'communication_tips': [
                {
                    'tip': 'Be Clear and Concise',
                    'explanation': 'Clearly state the problem in the first sentence',
                    'example': 'Instead of "My account is broken" say "I cannot login to my account since yesterday"'
                },
                {
                    'tip': 'Provide All Details',
                    'explanation': 'Include all relevant information upfront',
                    'example': 'Provide email, approximate date of issue, and what you\'ve tried'
                },
                {
                    'tip': 'Use Proper Formatting',
                    'explanation': 'Use paragraphs, bullet points for clarity',
                    'example': 'Separate different points into clear sections'
                },
                {
                    'tip': 'Remain Professional',
                    'explanation': 'Even if frustrated, maintain respectful tone',
                    'example': 'Avoid caps lock, excessive punctuation, or demands'
                }
            ],
            'follow_up_strategies': [
                {
                    'situation': 'No Response After 72 Hours',
                    'action': 'Send polite follow-up with reference number',
                    'template': 'Following up on case #[number] submitted on [date]'
                },
                {
                    'situation': 'Incomplete Response',
                    'action': 'Ask specific clarifying questions',
                    'template': 'Thank you for your response. Could you clarify [specific point]?'
                },
                {
                    'situation': 'Issue Not Resolved',
                    'action': 'Provide additional information or evidence',
                    'template': 'The suggested solution didn\'t work. Here\'s what happened when I tried...'
                },
                {
                    'situation': 'Wrong Department',
                    'action': 'Ask to be redirected to correct team',
                    'template': 'This appears to be a [different issue]. Could you transfer this to the appropriate team?'
                }
            ],
            'escalation_paths': [
                {
                    'level': 'Standard Support',
                    'when_to_use': 'Initial contact for most issues',
                    'expected_outcome': 'Resolution or proper routing'
                },
                {
                    'level': 'Supervisor/Manager',
                    'when_to_use': 'Standard support unhelpful or wrong',
                    'expected_outcome': 'Review and different approach'
                },
                {
                    'level': 'Executive Escalation',
                    'when_to_use': 'Critical issue unresolved for weeks',
                    'expected_outcome': 'Priority handling, possible compensation'
                },
                {
                    'level': 'Regulatory/Legal',
                    'when_to_use': 'Legal rights violated, data protection issues',
                    'expected_outcome': 'Formal investigation, compliance action'
                }
            ]
        }
        
        return tips
    
    def generate_support_template(self, issue_type):
        """সাপোর্ট টেম্পলেট জেনারেট"""
        templates = {
            'account_recovery': {
                'subject': 'Account Recovery Assistance - Unable to Login',
                'body': '''
Issue Description:
I am unable to access my Facebook account. When I try to login, I [describe what happens - e.g., get error message, password not working, etc.].

Account Information:
- Email/Phone associated: [your email/phone]
- Full name on account: [your full name]
- Date of birth: [your DOB]
- Approximate account creation: [month/year]

What I've Tried:
1. Password reset via email - [result]
2. Password reset via phone - [result]
3. Trusted contacts - [result]
4. ID verification - [result]

Additional Information:
- Last successful login: [date]
- Suspicious activity noticed: [yes/no details]
- Backup email: [if any]

I have attached [screenshots/ID] for verification.

Please help me recover access to my account.
                '''
            },
            'hacked_account': {
                'subject': 'URGENT: Account Compromised/Hacked',
                'body': '''
URGENT: My Facebook account has been hacked.

Account Information:
- Email: [your email]
- Phone: [your phone]
- Name: [your name]

Evidence of Compromise:
1. Unauthorized posts made on [date]
2. Password changed without my knowledge
3. Email/phone changed on account
4. Friends reporting strange messages

Timeline:
- Last legitimate access: [date/time]
- First noticed compromise: [date/time]
- Unauthorized changes noticed: [list changes]

Immediate Actions Taken:
1. Attempted password reset - [result]
2. Reported as hacked through facebook.com/hacked
3. Notified friends
4. Changed email password

I have attached screenshots of unauthorized activity.

Please secure my account immediately and restore my access.
                '''
            },
            'disabled_account': {
                'subject': 'Appeal for Disabled Account',
                'body': '''
Appeal for Disabled Account

Account Information:
- Name: [your full name]
- Email: [your email]
- Phone: [your phone]

I believe my account was disabled in error because:
[Explain why you believe it was an error]

I have reviewed Facebook's Community Standards and believe I have not violated them because:
[Explain your understanding and compliance]

To verify my identity, I have attached:
- Government-issued ID
- Additional proof if available

I understand the importance of Facebook's community standards and promise to comply with all rules if my account is restored.

Please review my appeal and restore my account access.
                '''
            }
        }
        
        return templates.get(issue_type, {'error': 'Template not found'})