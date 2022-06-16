from django.shortcuts import render, Http404
from . models import Post, Comment
from django.views import View
from django.views.generic import TemplateView, ListView
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


class StartingPageView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(author="Tim")
        return context


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]


class SinglePostView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        read_later_post = self.is_read_later(request, post)
        context = {
            "post": post,
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "read_later": read_later_post
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        read_later_post = self.is_read_later(request, post)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "read_later": read_later_post
        }
        return render(request, "blog/post-detail.html", context)

    def is_read_later(self, request, post):
        is_read_later = False
        if "read_later_posts" in request.session:
            for id in request.session["read_later_posts"]:
                if id == str(post.id):
                    is_read_later = True

        return is_read_later


class ReadLaterView(View):

    def post(self, request):
        post_id = request.POST["post_id"]

        if not "read_later_posts" in request.session or not request.session['read_later_posts']:
            request.session["read_later_posts"] = []
            request.session["read_later_posts"].append(post_id)

        else:
            posts_list = request.session['read_later_posts']
            posts_list.append(post_id)
            request.session['read_later_posts'] = posts_list


        return HttpResponseRedirect("read-later")

    def get(self, request):
        if not "read_later_posts" in request.session or not request.session['read_later_posts']:
            posts = []
        else:
            posts = self.get_read_later_posts(request)

        context = {
            "posts": posts
        }

        return render(request, "blog/read-later.html", context)

    def get_read_later_posts(self, request):
        posts = []
        for pk in request.session["read_later_posts"]:
            print(request.session["read_later_posts"])

            posts.append(Post.objects.get(id=pk))

        return posts


class RemoveFromReadLaterView(View):

    def get(self, request):
        return render(request, "blog/read-later.html")

    def post(self, request):
        m = request.session["read_later_posts"]
        try:
            m.remove(request.POST["post_id"])
        except:
            del request.session["read_later_posts"]

        request.session.modified = True
        return HttpResponseRedirect("read-later")


class AddPostView(View):

    def get(self, request):
        context = {
            "post_form": PostForm()
        }
        return render(request, "blog/add-post.html", context)

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        context = {
            "post_form": post_form
        }
        if post_form.is_valid():
            post_form.save()
            return HttpResponseRedirect("posts")

        return render(request, "blog/add-post.html", context)