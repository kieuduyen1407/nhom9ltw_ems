from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		widgets = {'first_name': forms.TextInput(attrs={'class':'form-control'}),
				   'last_name': forms.TextInput(attrs={'class':'form-control'}),
				   'email': forms.TextInput(attrs={'class':'form-control'})}
		labels = {'first_name': 'Họ', 'last_name': 'Tên', 'email': 'Email'}


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['dob', 'address', 'phone_number']
		widgets = {'dob': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
				   'address': forms.TextInput(attrs={'class':'form-control'}),
				   'phone_number': forms.TextInput(attrs={'class':'form-control'})}
		labels = {'dob': 'Ngày sinh', 'address': 'Địa chỉ', 'phone_number': 'Số điện thoại'}



class SignInForm(forms.ModelForm):
	class Meta:
		model=User
		fields = ['username', 'password']


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(label="Họ", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label="Tên", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

	dob = forms.DateField(label="Ngày sinh", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
	phone_number = forms.CharField(label="Số điện thoại",max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
	address = forms.CharField(label="Địa chỉ", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].label = 'Tên đăng nhập'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].label = 'Mật khẩu'
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Mật khẩu phải hơn 8 ký tự.</li><li>Mật khẩu không được toàn số.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].label = 'Nhập lại mật khẩu'
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Nhập lại mật khẩu để xác minh.</small></span>'