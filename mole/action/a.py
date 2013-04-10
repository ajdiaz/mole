d={}

x = type('Example', (object,), {
    "__init__": lambda x,y: y,
    "name": "andres",
})

z = x()
print z.metodo("hola")

