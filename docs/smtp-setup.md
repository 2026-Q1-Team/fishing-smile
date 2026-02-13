# Setup

## Prerequisite

A Google account with 2-Step Verification enabled.

+ Setting up a Google account. Step-by-step guide [here](https://support.google.com/accounts/answer/27441).
+ Enabling 2-Step Verification on your Google account. Step-by-step
  guide [here](https://support.google.com/accounts/answer/185839).

### Creating a Google account App password.

An app password is required for sending emails through Google SMTP servers.

+ Open your [Google account security menu](https://myaccount.google.com/security).
+ Locate and click the **2-Step-Verification** option.
+ Locate and click the **App passwords** option.
+ Enter a name into the **App name** field.
+ Click the **Create** button.
+ Copy the new app password and store it somewhere safe.

### Using the Google account App password.

In ``/dev/local-test/env/local-test.env``, locate entry:

```
FISHING_SMILE_CAST_SENDER='%EMAIL'
FISHING_SMILE_CAST_PASSWORD='%PASSWORD'
```

Replace ``%EMAIL`` & ``%PASSWORD`` with your Google account email address and app password.

**IMPORTANT** : This method limits the amount of emails that can be sent to 2,000 emails per day according
to [this](https://support.google.com/a/answer/176600) Google support article.