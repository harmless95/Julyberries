03.10.2025
    1. Закончить CRUD в reviews service - [v]
    2. Изучить как работает сеть по которой общаются контейнеры. И сделать сеть одну - [x]
    3. Протестировать авторизацию в куки для упрощения запросов и возможность обращаться на /docs - [x]
```
    ab -k -c 5 -n 20000 http://localhost:5354/; `
    ab -k -c 5 -n 2000 http://localhost:5354/status/400; `
    ab -k -c 5 -n 3000 http://localhost:5354/status/409; `
    ab -k -c 5 -n 5000 http://localhost:5354/status/500; `
    ab -k -c 50 -n 5000 "http://localhost:5354/status/200?seconds_sleep=1"; `
    ab -k -c 50 -n 2000 "http://localhost:5354/status/200?seconds_sleep=2"
```