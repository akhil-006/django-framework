from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    return render(request, "accounts/home.html", {})


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        # print(username, fname, lname, pass1, pass2, email)

        if User.objects.filter(username=username):
            messages.error(
                request,
                fail_silently=True,
                message=f"Username '{username}' already exists, "
                f"please try using another username",
            )
            return redirect("signup")

        if not username.isalnum():
            messages.error(
                request,
                message="Only alphanumeric usernames allowed",
                fail_silently=True,
            )
            return redirect("signup")

        permissible_len = 20
        if len(fname) > permissible_len:
            messages.error(
                request,
                fail_silently=True,
                message=f"Length of first name exceeds the "
                f"permissible limits: {permissible_len}",
            )
            return redirect("signup")

        if pass2 != pass1:
            messages.error(
                request,
                fail_silently=True,
                message="Passwords do not match! Please try again!",
            )

            return redirect("signup")

        # Create user after form validation
        try:
            user = User.objects.create_user(
                username=username,
                first_name=fname,
                last_name=lname,
                email=email,
                password=pass1,
            )
            user.save()

            messages.success(
                request=request,
                fail_silently=True,
                message="You have successfully sign-up. "
                "Please use your credentials to login.",
            )
            return redirect("home")
        except Exception as ex:
            messages.error(request, fail_silently=True, message=f"Error occurred: {ex}")

    return render(request, "accounts/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pass1"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, message="User logged in successfully!")
            return render(request, "accounts/home.html")
        else:
            messages.success(
                request, message="Invalid user! We can't let you in so easily!"
            )
            return redirect(to="home")

    return render(request, "accounts/signin.html")


def signout(request):
    user = request.user
    logout(request)
    messages.success(
        request, message=f"User {user} logged out successfully!", fail_silently=True
    )
    return redirect("home")
