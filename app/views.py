from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User, Feedback
from django.contrib.auth import login
from .forms import CustomUserCreationForm, FeedbackForm
from django.contrib.auth.views import LogoutView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'manager':
            return redirect('manager_dashboard')
        else:
            return redirect('employee_dashboard')
    return redirect('login')


@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('home')

    team = request.user.team_members.all()

    feedbacks = Feedback.objects.filter(manager=request.user)

    counts = {
        'positive': feedbacks.filter(sentiment='positive').count(),
        'neutral': feedbacks.filter(sentiment='neutral').count(),
        'negative': feedbacks.filter(sentiment='negative').count()
    }

    return render(request, 'manager_dashboard.html', {
        'team': team,
        'counts': counts
    })


@login_required
def employee_dashboard(request):
    if request.user.role != 'employee':
        return redirect('login')
    feedbacks = request.user.feedback_received.all()
    return render(request, 'employee_dashboard.html', {'feedbacks': feedbacks})


@login_required
def submit_feedback(request):
    if request.user.role != 'manager':
        return redirect('home')

    if request.method == 'POST':
        form = FeedbackForm(request.POST, manager=request.user)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.manager = request.user
            feedback.save()
            return redirect('manager_dashboard')
    else:
        form = FeedbackForm(manager=request.user)

    return render(request, 'submit_feedback.html', {'form': form})


@login_required
def acknowledge_feedback(request, feedback_id):
    if request.user.role != 'employee':
        return redirect('home')
    
    feedback = Feedback.objects.get(id=feedback_id, employee=request.user)
    if request.method == 'POST':
        feedback.acknowledged = True
        feedback.save()
    return redirect('employee_dashboard')


class LogoutViewAllowGet(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def edit_feedback(request, feedback_id):
    if request.user.role != 'manager':
        return redirect('home')

    feedback = Feedback.objects.get(id=feedback_id, manager=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback, manager=request.user)
        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
    else:
        form = FeedbackForm(instance=feedback, manager=request.user)

    return render(request, 'edit_feedback.html', {'form': form, 'feedback': feedback})


@login_required
def delete_feedback(request, feedback_id):
    if request.user.role != 'manager':
        return redirect('home')
    
    feedback = Feedback.objects.get(id=feedback_id, manager=request.user)
    
    if request.method == 'POST':
        feedback.delete()
        return redirect('manager_dashboard')
    
    return render(request, 'core/delete_feedback.html', {'feedback': feedback})


@login_required
def export_feedback_pdf(request, employee_id):
    if request.user.role != 'manager':
        return redirect('home')

    employee = User.objects.get(id=employee_id)
    if employee.manager != request.user:
        return HttpResponse("Unauthorized", status=403)

    feedbacks = Feedback.objects.filter(manager=request.user, employee=employee)

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=feedback_{employee.username}.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Feedback Report for {employee.username}")

    p.setFont("Helvetica", 12)
    y = height - 100

    if feedbacks.exists():
        for fb in feedbacks:
            p.drawString(50, y, f"Date: {fb.created_at.strftime('%Y-%m-%d %H:%M')} | Sentiment: {fb.sentiment}")
            y -= 20
            p.drawString(70, y, f"Strengths: {fb.strengths}")
            y -= 20
            p.drawString(70, y, f"Improvement Areas: {fb.improvement_areas}")
            y -= 40
            if y < 100:
                p.showPage()
                y = height - 100
    else:
        p.drawString(50, y, "No feedback available.")

    p.showPage()
    p.save()
    return response

