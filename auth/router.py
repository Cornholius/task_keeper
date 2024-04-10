from fastapi import APIRouter

router = APIRouter(
    prefix='/auth',
    tags=['Авторизация', 'Регистрация']
)


@router.get('/', tags=['Авторизация'])
def ololo():
    return


@router.get('/21')
def ololo2():
    return
