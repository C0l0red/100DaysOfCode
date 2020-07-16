from django import forms

class SendEmail(forms.Form):
    recepient = forms.EmailField(error_messages={'required': 'Email must be sent to someone',
                                            'invalid': 'Email is invalid'},
                            label="Email")
    subject = forms.CharField(label="Subject", 
                            error_messages={'required': 'Please enter an email'},
                            min_length=7,
                            strip=True)
    message = forms.CharField(widget=forms.Textarea,
                            label='Message',
                            min_length=10,
                            error_messages={'required': 'You must enter a message', 
                                            'min_length': 'Message can\'t be shorter than 20 characters'})

    def __str__(self):
        return self.Email