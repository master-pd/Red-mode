# file: recovery/email_recovery.py
import re
import json
from datetime import datetime

class EmailRecovery:
    """ইমেইল রিকভারি সিস্টেম"""
    
    def __init__(self):
        self.name = "Email Recovery System"
        
    def execute(self, recovery_request):
        """ইমেইল রিকভারি প্রসেস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            recovery_info = {
                'email_recovery_basics': self.get_email_recovery_basics(),
                'step_by_step_process': self.get_step_by_step_process(),
                'common_email_providers': self.get_common_email_providers(),
                'troubleshooting_guide': self.get_troubleshooting_guide(),
                'security_considerations': self.get_security_considerations(),
                'alternative_methods': self.get_email_alternative_methods()
            }
            
            results['data'] = recovery_info
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def get_email_recovery_basics(self):
        """ইমেইল রিকভারি বেসিকস"""
        basics = {
            'what_is_email_recovery': 'The process of regaining access to your Facebook account using the email address associated with it.',
            'when_to_use': [
                'You remember the email but forgot password',
                'You have access to the email inbox',
                'Phone number recovery is not working',
                'You want to change password',
                'Account security has been compromised'
            ],
            'prerequisites': [
                'Know the email address used for Facebook',
                'Have access to that email inbox',
                'Email account is still active',
                'Remember approximate account creation date',
                'Have basic account information'
            ],
            'success_factors': [
                'Email is still active and accessible',
                'You can receive emails at that address',
                'No suspicious activity on email account',
                'You remember account details',
                'Recovery email is not blocked or filtered'
            ]
        }
        
        return basics
    
    def get_step_by_step_process(self):
        """স্টেপ বাই স্টেপ প্রসেস"""
        process = {
            'preparation_steps': [
                {
                    'step': 1,
                    'action': 'Identify Your Email',
                    'details': 'Determine which email address you used for Facebook',
                    'tips': [
                        'Check old emails from Facebook',
                        'Try common email addresses you use',
                        'Ask friends what email they see on your profile'
                    ]
                },
                {
                    'step': 2,
                    'action': 'Check Email Accessibility',
                    'details': 'Ensure you can login to the email account',
                    'tips': [
                        'Test login to email provider',
                        'Check spam/junk folders',
                        'Verify email forwarding is working'
                    ]
                },
                {
                    'step': 3,
                    'action': 'Clear Browser Cache',
                    'details': 'Clear cookies and cache for fresh start',
                    'tips': [
                        'Use private/incognito mode',
                        'Clear Facebook cookies specifically',
                        'Try different browser'
                    ]
                }
            ],
            'recovery_steps': [
                {
                    'step': 1,
                    'action': 'Go to Facebook Login',
                    'details': 'Visit facebook.com and click "Forgotten account?"',
                    'expected_result': 'Account recovery page loads'
                },
                {
                    'step': 2,
                    'action': 'Enter Email Address',
                    'details': 'Type the email address associated with your account',
                    'expected_result': 'Facebook finds your account'
                },
                {
                    'step': 3,
                    'action': 'Choose Email Recovery',
                    'details': 'Select "Send email" or similar option',
                    'expected_result': 'Confirmation that email was sent'
                },
                {
                    'step': 4,
                    'action': 'Check Your Email',
                    'details': 'Open email from Facebook (check spam folder too)',
                    'expected_result': 'Find recovery email with link/code'
                },
                {
                    'step': 5,
                    'action': 'Click Recovery Link',
                    'details': 'Click the link in the email (expires after some time)',
                    'expected_result': 'Password reset page opens'
                },
                {
                    'step': 6,
                    'action': 'Create New Password',
                    'details': 'Enter and confirm a strong new password',
                    'expected_result': 'Password successfully changed'
                },
                {
                    'step': 7,
                    'action': 'Login with New Password',
                    'details': 'Use your email and new password to login',
                    'expected_result': 'Successful login to account'
                }
            ],
            'post_recovery_steps': [
                'Review account security settings',
                'Update recovery options',
                'Check for unauthorized activity',
                'Enable two-factor authentication',
                'Save backup recovery codes'
            ]
        }
        
        return process
    
    def get_common_email_providers(self):
        """কমন ইমেইল প্রোভাইডার্স"""
        providers = {
            'gmail': {
                'recovery_url': 'https://accounts.google.com/signin/recovery',
                'facebook_email_search': 'from:facebookmail.com OR from:facebook.com',
                'common_issues': [
                    'Emails going to spam',
                    'Account recovery delays',
                    'Two-factor authentication',
                    'Forwarding settings'
                ],
                'tips': [
                    'Check "All Mail" folder',
                    'Search for "Facebook" in emails',
                    'Check "Social" category',
                    'Look in "Promotions" tab'
                ]
            },
            'yahoo': {
                'recovery_url': 'https://login.yahoo.com/forgot',
                'facebook_email_search': 'from:facebook',
                'common_issues': [
                    'Account inactivity',
                    'Password reset limits',
                    'Security questions',
                    'Backup email required'
                ],
                'tips': [
                    'Check "Spam" folder',
                    'Look in "Bulk" folder',
                    'Search all folders',
                    'Check email forwarding'
                ]
            },
            'outlook_hotmail': {
                'recovery_url': 'https://account.live.com/resetpassword.aspx',
                'facebook_email_search': 'from:facebook',
                'common_issues': [
                    'Microsoft account linking',
                    'Security verification',
                    'Recovery code required',
                    'Account alias confusion'
                ],
                'tips': [
                    'Check "Junk Email" folder',
                    'Search "Facebook" in all folders',
                    'Check focused/other inbox',
                    'Verify account aliases'
                ]
            },
            'other_providers': {
                'aol': 'Check spam folder and search "Facebook"',
                'icloud': 'Check all devices and webmail',
                'protonmail': 'Check all folders including spam',
                'custom_domain': 'Contact domain administrator if needed'
            }
        }
        
        return providers
    
    def get_troubleshooting_guide(self):
        """ট্রাবলশুটিং গাইড"""
        troubleshooting = {
            'common_problems': [
                {
                    'problem': 'No recovery email received',
                    'possible_causes': [
                        'Email in spam/junk folder',
                        'Wrong email address entered',
                        'Email forwarding issues',
                        'Facebook email blocked',
                        'Email account full'
                    ],
                    'solutions': [
                        'Check spam and junk folders',
                        'Verify email address spelling',
                        'Wait 15-30 minutes',
                        'Try different email address',
                        'Clear email storage space'
                    ]
                },
                {
                    'problem': 'Recovery link expired',
                    'possible_causes': [
                        'Link clicked after expiration',
                        'Multiple reset requests',
                        'Security measures',
                        'Account compromised'
                    ],
                    'solutions': [
                        'Request new recovery email',
                        'Wait 24 hours if rate limited',
                        'Use phone recovery instead',
                        'Try trusted contacts method'
                    ]
                },
                {
                    'problem': 'Email account inaccessible',
                    'possible_causes': [
                        'Forgot email password',
                        'Email account hacked',
                        'Account deactivated',
                        'Provider issues'
                    ],
                    'solutions': [
                        'Recover email account first',
                        'Contact email provider support',
                        'Use alternative recovery methods',
                        'Try security questions'
                    ]
                },
                {
                    'problem': 'Wrong email on account',
                    'possible_causes': [
                        'Changed email and forgot',
                        'Used different email',
                        'Account created with wrong email',
                        'Email changed by hacker'
                    ],
                    'solutions': [
                        'Try all possible email addresses',
                        'Check with friends/family',
                        'Use phone number recovery',
                        'Try username instead'
                    ]
                }
            ],
            'advanced_troubleshooting': [
                {
                    'issue': 'Email loops back to login',
                    'fix': 'Clear all Facebook cookies and cache, use incognito mode'
                },
                {
                    'issue': "Can't find Facebook emails",
                    'fix': 'Search for "facebookmail.com" or "do-not-reply@facebook.com"'
                },
                {
                    'issue': 'Recovery page not loading',
                    'fix': 'Try different browser, disable extensions, check internet'
                },
                {
                    'issue': 'Security check required',
                    'fix': 'Complete CAPTCHA, verify identity, answer security questions'
                }
            ]
        }
        
        return troubleshooting
    
    def get_security_considerations(self):
        """সিকিউরিটি কনসিডারেশনস"""
        security = {
            'email_security_tips': [
                'Use strong, unique password for email',
                'Enable two-factor authentication on email',
                'Regularly update recovery options',
                'Monitor for suspicious activity',
                'Keep email software updated'
            ],
            'facebook_email_security': [
                'Facebook never asks for password via email',
                'Verify sender is from facebookmail.com',
                'Check URL before clicking links',
                'Look for your name in legitimate emails',
                'Report suspicious emails to Facebook'
            ],
            'prevent_future_lockouts': [
                'Add backup email addresses',
                'Set up trusted contacts',
                'Save recovery codes',
                'Use password manager',
                'Regularly update contact info'
            ],
            'warning_signs': [
                'Emails you don\'t recognize',
                'Password reset emails you didn\'t request',
                'Login alerts from unknown locations',
                'Friends reporting strange messages',
                'Profile changes you didn\'t make'
            ]
        }
        
        return security
    
    def get_email_alternative_methods(self):
        """ইমেইল অল্টারনেটিভ মেথডস"""
        alternatives = {
            'if_email_fails': [
                {
                    'method': 'Phone Number Recovery',
                    'requirements': 'Access to registered phone number',
                    'success_rate': '75%',
                    'steps': 'Use SMS code sent to your phone'
                },
                {
                    'method': 'Trusted Contacts',
                    'requirements': '3-5 friends set as trusted contacts',
                    'success_rate': '70%',
                    'steps': 'Get codes from trusted friends'
                },
                {
                    'method': 'ID Verification',
                    'requirements': 'Government-issued ID',
                    'success_rate': '85%',
                    'steps': 'Submit photos of valid ID'
                },
                {
                    'method': 'Security Questions',
                    'requirements': 'Remember security question answers',
                    'success_rate': '50%',
                    'steps': 'Answer pre-set security questions'
                }
            ],
            'contacting_support': [
                {
                    'channel': 'Facebook Help Center',
                    'response_time': '24-72 hours',
                    'best_for': 'General recovery issues'
                },
                {
                    'channel': 'Report Compromised Account',
                    'response_time': '12-48 hours',
                    'best_for': 'Hacked or compromised accounts'
                },
                {
                    'channel': 'Facebook Community Help',
                    'response_time': 'Varies',
                    'best_for': 'Peer advice and tips'
                }
            ]
        }
        
        return alternatives
    
    def check_email_validity(self, email):
        """ইমেইল ভ্যালিডিটি চেক"""
        validation = {
            'email': email,
            'is_valid_format': False,
            'domain_info': {},
            'suggestions': []
        }
        
        # Basic email format check
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            validation['is_valid_format'] = True
            
            # Extract domain
            domain = email.split('@')[1].lower()
            validation['domain'] = domain
            
            # Common email domains
            common_domains = {
                'gmail.com': {
                    'type': 'free',
                    'recovery': 'Google Account Recovery',
                    'notes': 'Check spam and all mail folders'
                },
                'yahoo.com': {
                    'type': 'free',
                    'recovery': 'Yahoo Account Recovery',
                    'notes': 'May have backup email or phone'
                },
                'outlook.com': {
                    'type': 'free',
                    'recovery': 'Microsoft Account Recovery',
                    'notes': 'Linked to Microsoft account'
                },
                'hotmail.com': {
                    'type': 'free',
                    'recovery': 'Microsoft Account Recovery',
                    'notes': 'Now part of Outlook'
                }
            }
            
            if domain in common_domains:
                validation['domain_info'] = common_domains[domain]
            else:
                validation['domain_info'] = {
                    'type': 'custom',
                    'recovery': 'Contact domain administrator',
                    'notes': 'May be work or custom email'
                }
        
        # Suggestions based on common mistakes
        common_mistakes = [
            ('gmai.com', 'gmail.com'),
            ('gmal.com', 'gmail.com'),
            ('yaho.com', 'yahoo.com'),
            ('outlok.com', 'outlook.com'),
            ('hotmai.com', 'hotmail.com')
        ]
        
        for wrong, correct in common_mistakes:
            if wrong in email.lower():
                suggestion = email.lower().replace(wrong, correct)
                validation['suggestions'].append(f'Try: {suggestion}')
        
        return validation
    
    def generate_recovery_email_template(self):
        """রিকভারি ইমেইল টেম্পলেট"""
        template = {
            'subject': 'Reset Your Facebook Password',
            'from': 'security@facebookmail.com',
            'body': '''
Hi [Your Name],

You recently asked to reset your Facebook password.

Click the link below to reset it:
[Recovery Link]

This link will expire in 24 hours. If you didn't request a password reset, you can ignore this email.

Thanks,
The Facebook Security Team

Facebook, Inc., Attention: Community Support, 1 Facebook Way, Menlo Park, CA 94025

To help keep your account secure, please don't forward this email. Learn more about keeping your Facebook account secure.
            ''',
            'security_indicators': [
                'Sender is from facebookmail.com domain',
                'Contains your name (not generic greeting)',
                'Link goes to facebook.com domain',
                'No request for personal information',
                'Includes physical address of Facebook'
            ],
            'warning_signs': [
                'Generic greeting like "Dear User"',
                'Links to non-facebook.com domains',
                'Requests for password or payment',
                'Poor spelling or grammar',
                'Urgent or threatening language'
            ]
        }
        
        return template