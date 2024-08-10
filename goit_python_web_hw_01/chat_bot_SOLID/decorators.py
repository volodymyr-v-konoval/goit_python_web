from functools import wraps



def input_error(func):
    '''
    This decorator catches errors in the chat-bot!
    '''
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Give me name and phone, please!'
        except IndexError:
            return 'Enter the argument for the command!'
        except KeyError:
            return "Sorry, I don't know the man!"
    
    return inner