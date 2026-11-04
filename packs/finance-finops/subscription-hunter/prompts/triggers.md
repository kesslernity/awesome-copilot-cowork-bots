# Event-driven task

**Supported, with a caveat.** Cowork event tasks fire on an incoming email, a Teams channel
message, or a Teams chat message. That is the whole list: there is no file, calendar or webhook
trigger, so this bot can only be triggered by mail arriving, not by a date approaching.

A useful trigger for this bot:

- **When:** you receive an email
- **Run in:** a new conversation
- **What it does:** If this message is a receipt, an invoice, a renewal notice or a trial-ending
  notice, add or update the vendor's row in the current subscriptions sheet, with a link to this
  message. Do not reply to it. If it is not one of those, do nothing and say nothing.

**The date-based job stays a scheduled prompt.** "Alert me 7 days before a renewal" cannot be an
event task, because the renewal date is not an event Cowork can see. The monthly schedule carries
that job instead.
