package authz

default allow = false

allow {
    ["HEAD", "OPTIONS"][_] = input.method
}
