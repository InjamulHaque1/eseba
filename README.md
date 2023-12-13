# eseba dependencies
	
	  Package          Version(or later)
	  ------------------------------------
	  asgiref          3.7.2
	  Django           5.0 -------> (install needed)
	  django-recaptcha 4.0.0 -----> (install needed)
	  Pillow           10.1.0 ----> (install needed)
	  pip              23.3.1
	  sqlparse         0.4.4
	  tzdata           2023.3

	Install pip(if pip gets uninstalled):
		1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		2. python get-pip.py

	Step 1: Remove all packages via pip(WARNING!!!! THIS WILL REMOVE ALL OF THE PACKAGES INSTALLED)
		pip freeze | xargs pip uninstall -y
  
		If 'xargs' is not recognised:
		pip freeze | ForEach-Object { pip uninstall -y $_.split('=')[0] }
  
		Method 2:
		pip freeze | ForEach-Object { pip uninstall -y ($_ -split '=')[0].Trim() }
  
		Method 3(Worked for me):
		for /f "tokens=1,* delims=^=" %i in ('pip freeze') do pip uninstall -y %i
  
	Step 2:	Install the mentioned packages from the avobe list
 		pip install django django-recaptcha pillow


-----Error handling-----
  1. Undefined path
  2. Login acccess


-----User-----
  1.	Registration (capctha)
  2.	Login (captcha)
  3.	Edit profile
  4.	Delete profile
  5.	Appointment History
  6.	Payment History


-----Product-----
  1.	Search
  2.	Buy 
  3.	Cart (update, remove)
  4.	Checkout


-----Appointment-----
  1.	Search doctors
  2.	Register
  3.	Cancel (in profile)
  4.	Support for unavailable doctors

-----Emergency-----
  1. Search blood in hospital
