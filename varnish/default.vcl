vcl 4.0;

backend default {
    .host = "book-review-app";
    .port = "8000";
}

sub vcl_recv {
    # Check if the request is for static or media files
    if (req.url ~ "^/static/" || req.url ~ "^/media/") {
        return (hash);
    }

    # Pass everything else directly to the backend (Django)
    return (pass);
}

sub vcl_backend_response {
    # Cache static and media files for 1 hour
    if (bereq.url ~ "^/static/" || bereq.url ~ "^/media/") {
        set beresp.ttl = 1h;
    }
}
