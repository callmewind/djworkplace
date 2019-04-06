#!/bin/bash

#Use sendgrid environment variables as default
export EMAIL_HOST_USER=${EMAIL_HOST_USER:-$SENDGRID_USERNAME}
export EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD:-$SENDGRID_PASSWORD}