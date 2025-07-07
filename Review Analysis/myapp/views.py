from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .scraper import scrape_reviews
from .summarizer import summarize_text


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            messages.success(request, "Account created! Please log in.")
            return redirect('login')

    return render(request, 'signup.html')


@login_required
def home_view(request):
    if request.method == 'POST':
        review_url = request.POST.get('review_url', '').strip()
        review_text = request.POST.get('review_text', '').strip()

        # Case 1: URL provided
        if review_url:
            review = scrape_reviews(review_url)
            source = 'URL'
        # Case 2: Manual input
        elif review_text:
            review = review_text
            source = 'Text Input'
        else:
            # Case 3: Nothing provided
            return render(request, 'home.html', {
                'error': "Please paste review text or provide a valid URL."
            })

        # Error handling
        if not review or "Unable to fetch" in review or "No reviews found" in review:
            return render(request, 'home.html', {
                'error': "Could not get valid reviews. Try another URL or paste text instead."
            })

        # Sentiment analysis
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(review)
        compound = score['compound']

        # Summarize
        summary = summarize_text(review)

        # Convert compound to percentage
        positive_percentage = int((compound + 1) * 50)

        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        return render(request, 'result.html', {
            'review': review,
            'sentiment': sentiment,
            'score': score,
            'source': source,
            'positive_percentage': positive_percentage,
            'summary': summary
        })

    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')
