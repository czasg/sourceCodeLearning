class BaseServer:
    """
    - __init__(server_address, RequestHandlerClass)
    - serve_forever(poll_interval=0.5)
    - shutdown()  -> Stops the serve_forever loop.
    - handle_request()  # if you do not use serve_forever(), is the top-level call.  It calls selector.select()
    - fileno() -> int   # for selector

    - server_bind()
    - server_activate()  -> Called by constructor to activate the server
    - get_request() -> request, client_address
    - handle_timeout()
    - verify_request(request, client_address)
    - server_close()
    - process_request(request, client_address) -> is the place that may fork a new process or create a
      new thread to finish the request
    - shutdown_request(request)
    - close_request(request)
    - service_actions()
    - handle_error()

    - service_actions() -> to implement any code that needs to be run during the loop.
    """


if __name__ == '__main__':
    with memoryview(b"cza is sg") as view:
        print(view.nbytes)