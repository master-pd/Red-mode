# file: recovery/password_reset.py
import json
import random
from datetime import datetime

class PasswordResetMethods:
    """পাসওয়ার্ড রিসেট মেথডস"""
    
    def __init__(self):
        self.name = "Password Reset Methods"
        
    def execute(self, reset_request):
        """পাসওয়ার্ড রিসেট মেথডস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            reset_info = {
                'reset_methods_overview': self.get_reset_methods_overview(),
                'step_by_step_guides': self.get_step_by_step_guides(),
                'password_security': self.get_password_security_info(),
                'common_problems': self.get_common_problems(),
                'advanced_troubleshooting': self.get_advanced_troubleshooting(),
                'prevention_tips': self.get_prevention_tips()
            }
            
            results['data'] = reset_info
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def get_reset_methods_overview(self):
        """রিসেট মেথডস ওভারভিউ"""
        overview = {
            'available_methods': [
                {
                    'method': 'Email Reset',
                    'description': 'Receive reset link via email',
                    'success_rate': '75%',
                    'time_required': '5-30 minutes',
                    'requirements': 'Access to registered email'
                },
                {
                    'method': 'SMS Reset',
                    'description': 'Receive code via SMS to phone',
                    'success_rate': '80%',
                    'time_required': '2-10 minutes',
                    'requirements': 'Access to registered phone'
                },
                {
                    'method': 'Trusted Contacts',
                    'description': 'Get codes from 3-5 trusted friends',
                    'success_rate': '70%',
                    'time_required': '15-60 minutes',
                    'requirements': 'Trusted contacts set up'
                },
                {
                    'method': 'Security Questions',
                    'description': 'Answer pre-set security questions',
                    'success_rate': '50%',
                    'time_required': '5-15 minutes',
                    'requirements': 'Remember security answers'
                },
                {
                    'method': 'ID Verification',
                    'description': 'Submit government ID for verification',
                    'success_rate': '85%',
                    'time_required': '24-72 hours',
                    'requirements': 'Valid government-issued ID'
                }
            ],
            'method_selection_guide': [
                {
                    'situation': 'Remember email/phone',
                    'recommended': 'Email or SMS reset',
                    'reason': 'Fastest and most straightforward'
                },
                {
                    'situation': 'No access to email/phone',
                    'recommended': 'Trusted contacts',
                    'reason': 'Uses social connections for recovery'
                },
                {
                    'situation': 'Account hacked',
                    'recommended': 'Hacked account form + ID verification',
                    'reason': 'Provides security verification'
                },
                {
                    'situation': 'All else fails',
                    'recommended': 'ID verification',
                    'reason': 'Most reliable but slowest'
                }
            ]
        }
        
        return overview
    
    def get_step_by_step_guides(self):
        """স্টেপ বাই স্টেপ গাইডস"""
        guides = {
            'email_reset_guide': [
                {
                    'step': 1,
                    'action': 'Go to Facebook Login Page',
                    'details': 'Visit facebook.com and click "Forgotten account?"'
                },
                {
                    'step': 2,
                    'action': 'Enter Your Email',
                    'details': 'Type the email address associated with your account'
                },
                {
                    'step': 3,
                    'action': 'Click "Search"',
                    'details': 'Facebook will search for your account'
                },
                {
                    'step': 4,
                    'action': 'Select Your Account',
                    'details': 'Click on your account from the search results'
                },
                {
                    'step': 5,
                    'action': 'Choose "Send Email"',
                    'details': 'Select the email reset option'
                },
                {
                    'step': 6,
                    'action': 'Check Your Email',
                    'details': 'Open the email from Facebook (check spam folder)'
                },
                {
                    'step': 7,
                    'action': 'Click Reset Link',
                    'details': 'Click the password reset link in the email'
                },
                {
                    'step': 8,
                    'action': 'Create New Password',
                    'details': 'Enter and confirm a strong new password'
                },
                {
                    'step': 9,
                    'action': 'Login with New Password',
                    'details': 'Use your email and new password to login'
                }
            ],
            'sms_reset_guide': [
                {
                    'step': 1,
                    'action': 'Go to Facebook Login Page',
                    'details': 'Visit facebook.com and click "Forgotten account?"'
                },
                {
                    'step': 2,
                    'action': 'Enter Your Phone Number',
                    'details': 'Type the phone number associated with your account'
                },
                {
                    'step': 3,
                    'action': 'Click "Search"',
                    'details': 'Facebook will search for your account'
                },
                {
                    'step': 4,
                    'action': 'Select Your Account',
                    'details': 'Click on your account from the search results'
                },
                {
                    'step': 5,
                    'action': 'Choose "Send SMS"',
                    'details': 'Select the SMS reset option'
                },
                {
                    'step': 6,
                    'action': 'Check Your Phone',
                    'details': 'Look for SMS from Facebook with reset code'
                },
                {
                    'step': 7,
                    'action': 'Enter Reset Code',
                    'details': 'Enter the 6-digit code from SMS'
                },
                {
                    'step': 8,
                    'action': 'Create New Password',
                    'details': 'Enter and confirm a strong new password'
                }
            ],
            'trusted_contacts_guide': [
                {
                    'step': 1,
                    'action': 'Go to Facebook Login Page',
                    'details': 'Visit facebook.com and click "Forgotten account?"'
                },
                {
                    'step': 2,
                    'action': 'Enter Account Details',
                    'details': 'Enter email, phone, or username'
                },
                {
                    'step': 3,
                    'action': 'Select "No longer have access to these?"',
                    'details': 'When asked how to reset password'
                },
                {
                    'step': 4,
                    'action': 'Choose "Reveal My Trusted Contacts"',
                    'details': 'Select this recovery option'
                },
                {
                    'step': 5,
                    'action': 'Enter Friend\'s Name',
                    'details': 'Enter full name of one trusted contact'
                },
                {
                    'step': 6,
                    'action': 'Contact Your Friends',
                    'details': 'Ask 3 trusted contacts for their codes'
                },
                {
                    'step': 7,
                    'action': 'Enter Recovery Codes',
                    'details': 'Enter codes from 3 different friends'
                },
                {
                    'step': 8,
                    'action': 'Reset Password',
                    'details': 'Create a new strong password'
                }
            ]
        }
        
        return guides
    
    def get_password_security_info(self):
        """পাসওয়ার্ড সিকিউরিটি ইনফো"""
        security = {
            'password_requirements': [
                'Minimum 6 characters (recommended 12+)',
                'Mix of uppercase and lowercase letters',
                'Include numbers (0-9)',
                'Include special characters (!@#$%^&*)',
                'No common words or patterns',
                'No personal information'
            ],
            'strong_password_examples': [
                'C0mpl3x!P@ssw0rd2024',
                'Blu3$ky#M0untain@123',
                'T3mp3r@ture*Rainbow99',
                'F1r3w0rk$!Celebrate42'
            ],
            'weak_password_examples': [
                'password123',
                '123456789',
                'qwertyuiop',
                'iloveyou',
                'admin123',
                'letmein'
            ],
            'password_manager_recommendations': [
                'LastPass',
                '1Password',
                'Bitwarden',
                'Dashlane',
                'Keeper'
            ],
            'password_hygiene': [
                'Change passwords every 3-6 months',
                'Use different passwords for different sites',
                'Never share passwords via email/text',
                'Use password manager to generate/store',
                'Enable two-factor authentication'
            ]
        }
        
        return security
    
    def get_common_problems(self):
        """কমন প্রব্লেমস"""
        problems = {
            'reset_link_issues': [
                {
                    'problem': 'Reset link not received',
                    'causes': [
                        'Email in spam/junk folder',
                        'Wrong email address entered',
                        'Email account full',
                        'Facebook email blocked',
                        'Technical delays'
                    ],
                    'solutions': [
                        'Check spam and junk folders',
                        'Wait 15-30 minutes',
                        'Verify email address spelling',
                        'Clear email storage space',
                        'Try SMS reset instead'
                    ]
                },
                {
                    'problem': 'Reset link expired',
                    'causes': [
                        'Link clicked after 24 hours',
                        'Multiple reset requests',
                        'Security measures triggered',
                        'Account compromised'
                    ],
                    'solutions': [
                        'Request new reset link',
                        'Wait 24 hours if rate limited',
                        'Use different reset method',
                        'Check account security'
                    ]
                },
                {
                    'problem': 'Link takes to wrong page',
                    'causes': [
                        'Browser cache issues',
                        'URL corruption',
                        'Security software interference',
                        'Network problems'
                    ],
                    'solutions': [
                        'Clear browser cache and cookies',
                        'Copy-paste link directly',
                        'Try different browser',
                        'Check URL starts with facebook.com'
                    ]
                }
            ],
            'sms_code_issues': [
                {
                    'problem': 'SMS not received',
                    'causes': [
                        'Wrong phone number',
                        'Carrier delays',
                        'Phone blocked Facebook SMS',
                        'International number issues',
                        'Phone number changed'
                    ],
                    'solutions': [
                        'Verify phone number',
                        'Wait 5-10 minutes',
                        'Check carrier message blocking',
                        'Try email reset instead',
                        'Contact mobile provider'
                    ]
                },
                {
                    'problem': 'Code not working',
                    'causes': [
                        'Code entered incorrectly',
                        'Code expired (5-10 minutes)',
                        'Multiple codes requested',
                        'Wrong account selected'
                    ],
                    'solutions': [
                        'Double-check code entry',
                        'Request new code',
                        'Wait for new code expiration',
                        'Verify correct account'
                    ]
                }
            ]
        }
        
        return problems
    
    def get_advanced_troubleshooting(self):
        """অ্যাডভান্সড ট্রাবলশুটিং"""
        advanced = {
            'browser_specific_issues': [
                {
                    'browser': 'Chrome',
                    'common_issues': [
                        'Extensions blocking Facebook',
                        'Cache corruption',
                        'Cookie settings too strict'
                    ],
                    'solutions': [
                        'Disable extensions temporarily',
                        'Clear browsing data completely',
                        'Allow third-party cookies'
                    ]
                },
                {
                    'browser': 'Firefox',
                    'common_issues': [
                        'Enhanced tracking protection',
                        'Cookie exceptions needed',
                        'Cache persistence'
                    ],
                    'solutions': [
                        'Disable tracking protection for Facebook',
                        'Add Facebook to cookie exceptions',
                        'Clear site data for Facebook'
                    ]
                },
                {
                    'browser': 'Safari',
                    'common_issues': [
                        'Intelligent tracking prevention',
                        'Privacy settings blocking',
                        'iCloud keychain issues'
                    ],
                    'solutions': [
                        'Disable tracking prevention for Facebook',
                        'Adjust privacy settings',
                        'Check iCloud keychain sync'
                    ]
                }
            ],
            'network_issues': [
                {
                    'issue': 'Firewall blocking',
                    'solution': 'Temporarily disable firewall or add Facebook exception',
                    'test': 'Try different network (mobile data)'
                },
                {
                    'issue': 'VPN interference',
                    'solution': 'Disconnect VPN temporarily',
                    'test': 'Access without VPN'
                },
                {
                    'issue': 'DNS problems',
                    'solution': 'Flush DNS cache or use different DNS',
                    'test': 'Try 8.8.8.8 (Google DNS)'
                },
                {
                    'issue': 'ISP blocking',
                    'solution': 'Contact ISP or use different network',
                    'test': 'Try mobile hotspot'
                }
            ],
            'account_specific_issues': [
                {
                    'issue': 'Account temporarily locked',
                    'cause': 'Multiple failed login attempts',
                    'solution': 'Wait 24 hours or use account recovery'
                },
                {
                    'issue': 'Password reset disabled',
                    'cause': 'Security concerns or hacking attempts',
                    'solution': 'Use ID verification or wait for review'
                },
                {
                    'issue': 'Email/phone changed by hacker',
                    'cause': 'Account compromised',
                    'solution': 'Use hacked account form and ID verification'
                }
            ]
        }
        
        return advanced
    
    def get_prevention_tips(self):
        """প্রিভেনশন টিপস"""
        prevention = {
            'proactive_measures': [
                {
                    'measure': 'Set Up Multiple Recovery Options',
                    'importance': 'High',
                    'how_to': 'Add backup email, phone, and trusted contacts'
                },
                {
                    'measure': 'Use Password Manager',
                    'importance': 'High',
                    'how_to': 'Generate and store strong, unique passwords'
                },
                {
                    'measure': 'Enable Two-Factor Authentication',
                    'importance': 'Critical',
                    'how_to': 'Use authenticator app or security key'
                },
                {
                    'measure': 'Regular Security Checkups',
                    'importance': 'Medium',
                    'how_to': 'Review login activity and security settings monthly'
                },
                {
                    'measure': 'Keep Contact Info Updated',
                    'importance': 'High',
                    'how_to': 'Update email and phone when they change'
                }
            ],
            'security_habits': [
                'Never share passwords with anyone',
                'Log out from shared computers',
                'Be wary of phishing emails',
                'Check login alerts regularly',
                'Use secure networks for login'
            ],
            'emergency_preparation': [
                'Save backup recovery codes',
                'Keep ID documents accessible',
                'Maintain relationships with trusted contacts',
                'Have alternative contact methods',
                'Know Facebook support channels'
            ]
        }
        
        return prevention
    
    def generate_password_suggestions(self, length=12):
        """পাসওয়ার্ড সাজেশন জেনারেট"""
        suggestions = []
        
        character_sets = {
            'lowercase': 'abcdefghijklmnopqrstuvwxyz',
            'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'numbers': '0123456789',
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
        
        for i in range(5):  # Generate 5 suggestions
            password = []
            
            # Ensure at least one from each character set
            password.append(random.choice(character_sets['lowercase']))
            password.append(random.choice(character_sets['uppercase']))
            password.append(random.choice(character_sets['numbers']))
            password.append(random.choice(character_sets['special']))
            
            # Fill remaining characters randomly
            all_chars = ''.join(character_sets.values())
            for _ in range(length - 4):
                password.append(random.choice(all_chars))
            
            # Shuffle the password
            random.shuffle(password)
            suggestions.append(''.join(password))
        
        return {
            'password_length': length,
            'suggestions': suggestions,
            'strength_indicators': [
                'Contains uppercase and lowercase',
                'Includes numbers and special characters',
                'No dictionary words',
                'No sequential patterns',
                'No personal information'
            ]
        }
    
    def check_password_strength(self, password):
        """পাসওয়ার্ড স্ট্রেন্থ চেক"""
        strength = {
            'password': '***' + password[-3:] if len(password) > 3 else '***',
            'length_score': 0,
            'complexity_score': 0,
            'commonality_score': 0,
            'overall_score': 0,
            'recommendations': []
        }
        
        # Length check
        if len(password) >= 12:
            strength['length_score'] = 30
        elif len(password) >= 8:
            strength['length_score'] = 20
        else:
            strength['length_score'] = 10
            strength['recommendations'].append('Use at least 8 characters (12+ recommended)')
        
        # Complexity check
        complexity_points = 0
        if any(c.islower() for c in password):
            complexity_points += 1
        if any(c.isupper() for c in password):
            complexity_points += 1
        if any(c.isdigit() for c in password):
            complexity_points += 1
        if any(not c.isalnum() for c in password):
            complexity_points += 1
        
        strength['complexity_score'] = complexity_points * 15
        
        if complexity_points < 4:
            strength['recommendations'].append('Include uppercase, lowercase, numbers, and special characters')
        
        # Common patterns check
        common_patterns = [
            'password', '123456', 'qwerty', 'admin', 'welcome',
            'login', 'abc123', 'letmein', 'monkey', 'dragon'
        ]
        
        password_lower = password.lower()
        is_common = any(pattern in password_lower for pattern in common_patterns)
        
        if not is_common:
            strength['commonality_score'] = 25
        else:
            strength['commonality_score'] = 5
            strength['recommendations'].append('Avoid common words and patterns')
        
        # Calculate overall score
        strength['overall_score'] = strength['length_score'] + strength['complexity_score'] + strength['commonality_score']
        
        # Rating
        if strength['overall_score'] >= 80:
            strength['rating'] = 'Strong'
        elif strength['overall_score'] >= 60:
            strength['rating'] = 'Good'
        elif strength['overall_score'] >= 40:
            strength['rating'] = 'Weak'
        else:
            strength['rating'] = 'Very Weak'
        
        return strength