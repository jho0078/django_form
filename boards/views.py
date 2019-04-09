from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {
        'boards' : boards
    }
    return render(request, 'boards/index.html', context)

@login_required
def create(request):
    # POST 요청이면 FORM 데이터를 처리한다.
    if request.method == 'POST':
        # 이 처리과정은 "binding" 으로 불리는데, 폼의 유효성 체크를 할 수 있도록 해준다.
        form = BoardForm(request.POST)
        # form 유효성 체크
        if form.is_valid():
            board = form.save()
            return redirect('boards:detail', board.pk)
    # GET 요청(혹은 다른 메서드)이면 기본 폼을 생성한다.
    else:
        form = BoardForm()
    context = {'form' : form}
    return render(request, 'boards/form.html', context)
        
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    context = {
        'board' : board
    }
    return render(request, 'boards/detail.html', context)
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
    else:
        return redirect('boards:detail', board.pk)
        
@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board) # 1
        if form.is_valid():
            board = form.save()                        # 2
            return redirect('boards:detail', board.pk)
    # GET 요청이면(수정하기 버튼을 눌렀을 때)
    else:
        # BoardForm 을 초기화(사용자 입력 값을 넣어준 상태로)
        # form = BoardForm(initial={'title': board.title, 'content': board.content})
        form = BoardForm(instance=board)               # 3
    
    # 1. POST : 요청에서 검증에 실패하였을 때, 오류 메세지가 포함된 상태
    # 2. GET : 요청에서 초기화된 상태
    context = {'form': form, 'board': board,}
    return render(request, 'boards/form.html', context)