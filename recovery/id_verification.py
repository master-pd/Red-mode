# file: recovery/id_verification.py
import json
import re
from datetime import datetime

class IDVerification:
    """আইডি ভেরিফিকেশন সিস্টেম"""
    
    def __init__(self):
        self.name = "ID Verification System"
        
    def execute(self, user_info):
        """আইডি ভেরিফিকেশন প্রসেস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            verification = {
                'verification_steps': self.get_verification_steps(),
                'required_documents': self.get_required_documents(),
                'common_issues': self.get_common_issues(),
                'verification_tips': self.get_verification_tips(),
                'facebook_specific': self.facebook_verification_info(),
                'alternative_methods': self.get_alternative_methods()
            }
            
            results['data'] = verification
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def get_verification_steps(self):
        """ভেরিফিকেশন স্টেপস"""
        steps = [
            {
                'step': 1,
                'title': 'Prepare Your Documents',
                'description': 'Collect government-issued ID (passport, driver\'s license, national ID)',
                'time_required': '5-10 minutes',
                'important_notes': [
                    'Document must be clearly visible',
                    'All four corners should be visible',
                    'Information must match your Facebook profile'
                ]
            },
            {
                'step': 2,
                'title': 'Access Facebook Help Center',
                'description': 'Go to Facebook Help Center and find "ID Verification" section',
                'time_required': '2-5 minutes',
                'important_notes': [
                    'Use the same device you normally access Facebook from',
                    'Make sure you\'re logged into your account'
                ]
            },
            {
                'step': 3,
                'title': 'Upload Your ID',
                'description': 'Follow the prompts to upload photos of your ID',
                'time_required': '5-15 minutes',
                'important_notes': [
                    'Take clear photos in good lighting',
                    'Upload both front and back if required',
                    'File formats: JPG, PNG, PDF'
                ]
            },
            {
                'step': 4,
                'title': 'Submit and Wait',
                'description': 'Submit the verification request and wait for review',
                'time_required': '24-72 hours',
                'important_notes': [
                    'Do not submit multiple requests',
                    'Check your email for updates',
                    'Review may take longer during busy periods'
                ]
            },
            {
                'step': 5,
                'title': 'Follow Up if Needed',
                'description': 'If not verified, follow up with additional information',
                'time_required': 'Varies',
                'important_notes': [
                    'Check why verification failed',
                    'Provide additional documents if requested',
                    'Be patient with the process'
                ]
            }
        ]
        
        return steps
    
    def get_required_documents(self):
        """প্রয়োজনীয় ডকুমেন্টস"""
        documents = {
            'primary_documents': [
                {
                    'name': 'Passport',
                    'acceptance_rate': '95%',
                    'requirements': [
                        'Clear photo of information page',
                        'Photo must be in color',
                        'All text must be readable'
                    ]
                },
                {
                    'name': 'Driver\'s License',
                    'acceptance_rate': '90%',
                    'requirements': [
                        'Front and back photos',
                        'Must be valid (not expired)',
                        'Issued by government authority'
                    ]
                },
                {
                    'name': 'National ID Card',
                    'acceptance_rate': '85%',
                    'requirements': [
                        'Clear photo of both sides',
                        'Issued by government',
                        'Must include photo and date of birth'
                    ]
                }
            ],
            'secondary_documents': [
                {
                    'name': 'Birth Certificate',
                    'acceptance_rate': '70%',
                    'when_to_use': 'When primary documents are unavailable'
                },
                {
                    'name': 'Voter ID Card',
                    'acceptance_rate': '75%',
                    'when_to_use': 'For citizens with voting rights'
                },
                {
                    'name': 'Student ID',
                    'acceptance_rate': '60%',
                    'when_to_use': 'For students with government-issued student ID'
                }
            ],
            'supporting_documents': [
                'Utility bill (electricity, water, gas)',
                'Bank statement',
                'Official letter with address',
                'Tax documents',
                'Insurance documents'
            ]
        }
        
        return documents
    
    def get_common_issues(self):
        """কমন ইস্যু এবং সমাধান"""
        issues = [
            {
                'issue': 'ID photo is blurry',
                'solution': 'Take photo in good lighting, ensure camera is steady',
                'prevention': 'Use phone with good camera quality, natural light is best'
            },
            {
                'issue': 'ID information doesn\'t match profile',
                'solution': 'Update Facebook profile to match ID information',
                'prevention': 'Use legal name on Facebook that matches official documents'
            },
            {
                'issue': 'ID is expired',
                'solution': 'Use a valid, non-expired ID',
                'prevention': 'Check expiration date before submitting'
            },
            {
                'issue': 'Document not accepted',
                'solution': 'Try a different type of government-issued ID',
                'prevention': 'Use passport or driver\'s license when possible'
            },
            {
                'issue': 'Verification taking too long',
                'solution': 'Wait 72 hours, then check email for updates',
                'prevention': 'Submit during business hours, avoid weekends'
            }
        ]
        
        return issues
    
    def get_verification_tips(self):
        """ভেরিফিকেশন টিপস"""
        tips = {
            'general_tips': [
                'Use high-quality photos (at least 1MB file size)',
                'Ensure all text is readable',
                'Remove any covers or cases from ID',
                'Take photos against a plain, contrasting background',
                'Do not edit or filter the photos'
            ],
            'privacy_tips': [
                'Facebook encrypts your ID information',
                'Photos are deleted after verification',
                'Only share with official Facebook channels',
                'Never share ID via email or messenger',
                'Verify you\'re on official Facebook website'
            ],
            'technical_tips': [
                'Use JPEG or PNG format',
                'File size should be 1-5MB',
                'Resolution: at least 720x720 pixels',
                'Use original photos, not screenshots',
                'Check file is not corrupted'
            ]
        }
        
        return tips
    
    def facebook_verification_info(self):
        """ফেসবুক স্পেসিফিক ইনফো"""
        facebook_info = {
            'official_links': [
                'https://www.facebook.com/help/contact/606967319425038',
                'https://www.facebook.com/help/159096464162185',
                'https://www.facebook.com/help/105487009541643'
            ],
            'verification_types': [
                {
                    'type': 'Account Recovery',
                    'purpose': 'Regain access to locked account',
                    'success_rate': '85%'
                },
                {
                    'type': 'Identity Confirmation',
                    'purpose': 'Confirm account ownership',
                    'success_rate': '90%'
                },
                {
                    'type': 'Business Verification',
                    'purpose': 'Verify business or page',
                    'success_rate': '80%'
                }
            ],
            'contact_methods': [
                {
                    'method': 'Facebook Help Center',
                    'response_time': '24-72 hours',
                    'best_for': 'General verification issues'
                },
                {
                    'method': 'Official Facebook Email',
                    'response_time': '48-96 hours',
                    'best_for': 'Follow-up on submitted cases'
                },
                {
                    'method': 'Trusted Contacts',
                    'response_time': '1-24 hours',
                    'best_for': 'Account recovery without ID'
                }
            ]
        }
        
        return facebook_info
    
    def get_alternative_methods(self):
        """অল্টারনেটিভ মেথডস"""
        alternatives = [
            {
                'method': 'Trusted Contacts',
                'description': 'Use 3-5 friends to verify your identity',
                'success_rate': '70%',
                'requirements': [
                    'Pre-set trusted contacts',
                    'Friends must have Facebook accounts',
                    'Friends must be accessible'
                ],
                'steps': [
                    'Click "Forgot Password"',
                    'Select "No longer have access to these?"',
                    'Choose "Reveal My Trusted Contacts"',
                    'Contact your friends for codes',
                    'Enter codes to recover account'
                ]
            },
            {
                'method': 'Email/Phone Verification',
                'description': 'Use associated email or phone number',
                'success_rate': '60%',
                'requirements': [
                    'Access to registered email/phone',
                    'Email/phone still active',
                    'Remember which one was used'
                ]
            },
            {
                'method': 'Security Questions',
                'description': 'Answer pre-set security questions',
                'success_rate': '50%',
                'requirements': [
                    'Remember answers to questions',
                    'Questions were set up previously',
                    'Answers match exactly'
                ]
            },
            {
                'method': 'Login Approvals',
                'description': 'Use two-factor authentication codes',
                'success_rate': '80%',
                'requirements': [
                    '2FA was enabled',
                    'Access to authentication device',
                    'Backup codes available'
                ]
            }
        ]
        
        return alternatives
    
    def verify_document_quality(self, document_info):
        """ডকুমেন্ট কোয়ালিটি ভেরিফিকেশন"""
        quality_check = {
            'passed_checks': [],
            'failed_checks': [],
            'score': 0,
            'recommendations': []
        }
        
        checks = [
            ('document_type', self.check_document_type(document_info.get('type', ''))),
            ('expiry_date', self.check_expiry_date(document_info.get('expiry', ''))),
            ('photo_quality', self.check_photo_quality(document_info.get('photo_quality', ''))),
            ('information_completeness', self.check_information_completeness(document_info)),
            ('legibility', self.check_legibility(document_info.get('legibility_score', 0)))
        ]
        
        passed = 0
        for check_name, result in checks:
            if result['passed']:
                quality_check['passed_checks'].append(check_name)
                passed += 1
            else:
                quality_check['failed_checks'].append({
                    'check': check_name,
                    'reason': result.get('reason', '')
                })
                quality_check['recommendations'].append(result.get('recommendation', ''))
        
        quality_check['score'] = (passed / len(checks)) * 100
        
        return quality_check
    
    def check_document_type(self, doc_type):
        """ডকুমেন্ট টাইপ চেক"""
        valid_types = ['passport', 'drivers_license', 'national_id', 'birth_certificate']
        
        if doc_type.lower() in valid_types:
            return {
                'passed': True,
                'message': f'{doc_type} is accepted by Facebook'
            }
        else:
            return {
                'passed': False,
                'reason': f'{doc_type} may not be accepted',
                'recommendation': 'Use passport, driver\'s license, or national ID'
            }
    
    def check_expiry_date(self, expiry_date):
        """এক্সপায়ারি ডেট চেক"""
        if not expiry_date:
            return {'passed': True, 'message': 'No expiry date provided'}
        
        try:
            expiry = datetime.strptime(expiry_date, '%Y-%m-%d')
            if expiry > datetime.now():
                return {'passed': True, 'message': 'Document is not expired'}
            else:
                return {
                    'passed': False,
                    'reason': 'Document is expired',
                    'recommendation': 'Use a valid, non-expired document'
                }
        except:
            return {'passed': True, 'message': 'Could not parse expiry date'}
    
    def check_photo_quality(self, quality):
        """ফটো কোয়ালিটি চেক"""
        if not quality:
            return {'passed': True, 'message': 'No quality info provided'}
        
        if quality.lower() in ['good', 'excellent', 'high']:
            return {'passed': True, 'message': 'Photo quality is good'}
        elif quality.lower() in ['poor', 'bad', 'low']:
            return {
                'passed': False,
                'reason': 'Photo quality is poor',
                'recommendation': 'Take clear photo in good lighting'
            }
        else:
            return {'passed': True, 'message': 'Photo quality acceptable'}
    
    def check_information_completeness(self, doc_info):
        """ইনফরমেশন কমপ্লিটনেস চেক"""
        required_fields = ['full_name', 'date_of_birth', 'document_number']
        missing = []
        
        for field in required_fields:
            if not doc_info.get(field):
                missing.append(field)
        
        if not missing:
            return {'passed': True, 'message': 'All required information present'}
        else:
            return {
                'passed': False,
                'reason': f'Missing fields: {", ".join(missing)}',
                'recommendation': 'Ensure document shows name, date of birth, and document number'
            }
    
    def check_legibility(self, score):
        """লেজিবিলিটি চেক"""
        if score >= 70:
            return {'passed': True, 'message': 'Document is legible'}
        elif score >= 50:
            return {
                'passed': False,
                'reason': 'Document legibility is marginal',
                'recommendation': 'Take clearer photo with better lighting'
            }
        else:
            return {
                'passed': False,
                'reason': 'Document is not legible',
                'recommendation': 'Retake photo ensuring all text is readable'
            }