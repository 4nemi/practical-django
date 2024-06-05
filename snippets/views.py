from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from snippets.models import Snippet, Comment
from snippets.forms import SnippetForm, CommentForm


# Create your views here.
def top(request):
    snippets = Snippet.objects.all()
    context = {"snippets": snippets}
    return render(request, "snippets/top.html", context)

@login_required
def snippet_new(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form = SnippetForm()
    return render(request, "snippets/snippet_new.html", {"form": form})


@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません。")

    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect("snippet_detail", snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, "snippets/snippet_edit.html", {"form": form})


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    comments = Comment.objects.filter(commented_to=snippet)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL + f"?next={request.path}")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented_to = snippet
            comment.commented_by = request.user
            comment.save()
            return redirect(snippet_detail, snippet_id=snippet.id)
    else:
        form = CommentForm()
            
    return render(request, "snippets/snippet_detail.html", {"snippet": snippet, "comments": comments, "form": form})


@login_required
def comment_new(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented_to = snippet
            comment.commented_by = request.user
            comment.save()
            return redirect(snippet_detail, snippet_id=snippet_id)
    else:
        form = CommentForm()
    return render(request, "snippets/comment_new.html", {"snippet": snippet, "form": form})


def handler400(request, exception):
    return render(request, 'errors/400.html', {}, status=400)


def handler403(request, exception):
    return render(request, 'errors/403.html', {}, status=403)


def handler404(request, exception):
    return render(request, 'errors/404.html', {}, status=404)


def handler500(request):
    return render(request, 'errors/500.html', {}, status=500)

