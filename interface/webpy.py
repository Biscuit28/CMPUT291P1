import web

render = web.template.render('templates/',  globals={"type": type})

urls = ('/',    'index',
        '/customer',    'customer',
        '/agent',    'agent'
        '/customer/login', 'clogin',
        '/customer/signup', 'signup')

class index:

    def GET(self):
        return render.index()

class customer:

    def GET(self):
        return render.customer()

class agent:

    def GET(self):
        return render.agent()

class clogin:

    def GET(self):
        pass

class signup:

    def GET(self)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
