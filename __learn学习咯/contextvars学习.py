from contextvars import *

# var= ContextVar('var')
#
# x=[1]
# var.set(x)
#
# y=var.get()
# print(f'x: {id(x)},y: {id(y)},{id(x)==id(y)}')
#
# y=var.get()
# print(f'x: {id(x)},y: {id(y)},{id(x)==id(y)}')
#
#
# z=[2]
#
# token=var.set(z)
# print(f'z: {var.get()}')
#
# var.reset(token)
#
# y=var.get()
# print(f'x: {id(x)},y: {id(y)},{id(x)==id(y)}')



var = ContextVar('var')
var.set('spam')

def main():
    # 'var' was set to 'spam' before
    # calling 'copy_context()' and 'ctx.run(main)', so:
    print(var.get() == ctx[var] == 'spam')

    var.set('ham')

    # Now, after setting 'var' to 'ham':
    print(var.get() == ctx[var] == 'ham')

ctx = copy_context()

# Any changes that the 'main' function makes to 'var'
# will be contained in 'ctx'.
ctx.run(main)

# The 'main()' function was run in the 'ctx' context,
# so changes to 'var' are contained in it:
print(ctx[var] == 'ham')

# However, outside of 'ctx', 'var' is still set to 'spam':
print(var.get() == 'spam')