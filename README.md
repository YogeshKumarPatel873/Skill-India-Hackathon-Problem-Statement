# Skill-India-Hackathon-Problem-Statement
Here we were tasked to create an application that can sent single mail or massage to many users at a time on single click


🎉 Features
🗜️ Small (~121 lines)
🐍 Pure Python
🔌 Working with multiple devices
📌 Save SMS as Draft
🔥 Delete SMS after sending
🌻 Motivation

Mail Demon is a simple and lightweight C# smtp server and mail list system for sending unlimited emails and text messages. With a focus on simplicity, async and performance, you'll be able to easily send thousands of messages per second even on a cheap Linux VPS. Memory usage and CPU usage are optimized to the max. Security and spam prevention is also built in using SPF validation.

Ensure you have setup DNS for your domain (TXT, A and MX record)
Setup SPF record: v=spf1 mx -all
Setup MX record: @ or smtp or email, etc.
Setup A and/or AAAA record: @ or smtp or email, etc.
Setup DMARC record, https://en.wikipedia.org/wiki/DMARC
Setup DKIM, https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail
Setup reverse dns for your ip address to your A and/or AAAA record. Your hosting provider should have a way to do this.


The error handling has been improved, the send to number is now verified and works with all countries that Telnyx supports.
The invalid phone numbers are displayed in a more user friendly way, giving the option to download them all as CSV or simply deleting them from the input field. These errors are split into three different categories:
Invalid Numbers
Missing country code
Duplicates
