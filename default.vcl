vcl 4.1;

backend default {
    .host = "book-review-app";
    .port = "8000";
}

sub vcl_recv {
    if (req.url ~ "^/static/") {
        return (hash);
    }

    if (req.method != "GET" && req.method != "HEAD") {
        return (pass);
    }
}

sub vcl_backend_response {
    set beresp.ttl = 24h;
    if (beresp.status >= 500) {
        return (pass);
    }
}
