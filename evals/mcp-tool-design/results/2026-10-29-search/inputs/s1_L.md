# Stage 1: find the tool

Host context: You are the assistant in a chat app with many connected tools. The user is Sam Ortiz, a support agent on the Billing team, timezone Europe/Berlin. Right now it is Thursday 2026-10-29, 14:00 in Berlin.

Your host shows you the names of 369 connected tools below, but not their descriptions or inputs. Before you can call a
tool you must load it with one search, in one of two forms:

- `select`: up to 5 exact tool names to load.
- `query`: keywords; the search matches them against tool names and descriptions and loads the 5 best matches. A word
  starting with `+` must appear in the tool name (for example `+helpdesk reply`).

## Connected tool names

- mcp__claude_ai_Cal_com__add_booking_attendee
- mcp__claude_ai_Cal_com__assign_attribute_to_user
- mcp__claude_ai_Cal_com__calculate_routing_form_slots
- mcp__claude_ai_Cal_com__call_api_operation
- mcp__claude_ai_Cal_com__cancel_booking
- mcp__claude_ai_Cal_com__confirm_booking
- mcp__claude_ai_Cal_com__confirm_booking_seats
- mcp__claude_ai_Cal_com__create_booking
- mcp__claude_ai_Cal_com__create_event_type
- mcp__claude_ai_Cal_com__create_org_membership
- mcp__claude_ai_Cal_com__create_routing_form
- mcp__claude_ai_Cal_com__create_schedule
- mcp__claude_ai_Cal_com__create_team_invite
- mcp__claude_ai_Cal_com__create_team_membership
- mcp__claude_ai_Cal_com__decline_booking_seats
- mcp__claude_ai_Cal_com__delete_event_type
- mcp__claude_ai_Cal_com__delete_org_membership
- mcp__claude_ai_Cal_com__delete_schedule
- mcp__claude_ai_Cal_com__delete_team_membership
- mcp__claude_ai_Cal_com__describe_api_operation
- mcp__claude_ai_Cal_com__duplicate_event_type
- mcp__claude_ai_Cal_com__edit_routing_form_fields
- mcp__claude_ai_Cal_com__edit_routing_form_routes
- mcp__claude_ai_Cal_com__find_api_operation
- mcp__claude_ai_Cal_com__get_app_link
- mcp__claude_ai_Cal_com__get_attribute_options
- mcp__claude_ai_Cal_com__get_availability
- mcp__claude_ai_Cal_com__get_booking
- mcp__claude_ai_Cal_com__get_booking_attendee
- mcp__claude_ai_Cal_com__get_booking_attendees
- mcp__claude_ai_Cal_com__get_booking_routing_trace
- mcp__claude_ai_Cal_com__get_bookings
- mcp__claude_ai_Cal_com__get_busy_times
- mcp__claude_ai_Cal_com__get_conferencing_apps
- mcp__claude_ai_Cal_com__get_connected_calendars
- mcp__claude_ai_Cal_com__get_crm_sync_errors
- mcp__claude_ai_Cal_com__get_default_schedule
- mcp__claude_ai_Cal_com__get_event
- mcp__claude_ai_Cal_com__get_event_type
- mcp__claude_ai_Cal_com__get_event_type_history
- mcp__claude_ai_Cal_com__get_event_type_settings
- mcp__claude_ai_Cal_com__get_event_types
- mcp__claude_ai_Cal_com__get_events
- mcp__claude_ai_Cal_com__get_me
- mcp__claude_ai_Cal_com__get_my_teams
- mcp__claude_ai_Cal_com__get_org_attribute
- mcp__claude_ai_Cal_com__get_org_attributes
- mcp__claude_ai_Cal_com__get_org_membership
- mcp__claude_ai_Cal_com__get_org_memberships
- mcp__claude_ai_Cal_com__get_org_routing_form_responses
- mcp__claude_ai_Cal_com__get_org_routing_forms
- mcp__claude_ai_Cal_com__get_org_team_bookings
- mcp__claude_ai_Cal_com__get_org_teams
- mcp__claude_ai_Cal_com__get_org_user_bookings
- mcp__claude_ai_Cal_com__get_routing_form
- mcp__claude_ai_Cal_com__get_routing_form_history
- mcp__claude_ai_Cal_com__get_schedule
- mcp__claude_ai_Cal_com__get_schedules
- mcp__claude_ai_Cal_com__get_scheduling_config
- mcp__claude_ai_Cal_com__get_team_membership
- mcp__claude_ai_Cal_com__get_team_memberships
- mcp__claude_ai_Cal_com__get_team_routing_forms
- mcp__claude_ai_Cal_com__get_user_attribute_history
- mcp__claude_ai_Cal_com__get_user_attributes
- mcp__claude_ai_Cal_com__mark_booking_absent
- mcp__claude_ai_Cal_com__reschedule_booking
- mcp__claude_ai_Cal_com__search_docs
- mcp__claude_ai_Cal_com__unassign_attribute_from_user
- mcp__claude_ai_Cal_com__update_event_type
- mcp__claude_ai_Cal_com__update_me
- mcp__claude_ai_Cal_com__update_org_membership
- mcp__claude_ai_Cal_com__update_schedule
- mcp__claude_ai_Cal_com__update_team_membership
- mcp__claude_ai_Cal_com__update_user_attribute
- mcp__claude_ai_Claude_Docs__batch
- mcp__claude_ai_Claude_Docs__create
- mcp__claude_ai_Claude_Docs__delete
- mcp__claude_ai_Claude_Docs__export
- mcp__claude_ai_Claude_Docs__guide
- mcp__claude_ai_Claude_Docs__query
- mcp__claude_ai_Claude_Docs__read
- mcp__claude_ai_Claude_Docs__update
- mcp__claude_ai_Gmail__apply_sensitive_message_label
- mcp__claude_ai_Gmail__apply_sensitive_thread_label
- mcp__claude_ai_Gmail__create_draft
- mcp__claude_ai_Gmail__create_label
- mcp__claude_ai_Gmail__delete_draft
- mcp__claude_ai_Gmail__delete_label
- mcp__claude_ai_Gmail__forward
- mcp__claude_ai_Gmail__get_draft
- mcp__claude_ai_Gmail__get_message
- mcp__claude_ai_Gmail__get_thread
- mcp__claude_ai_Gmail__label_message
- mcp__claude_ai_Gmail__label_thread
- mcp__claude_ai_Gmail__list_drafts
- mcp__claude_ai_Gmail__list_labels
- mcp__claude_ai_Gmail__mark_message_spam
- mcp__claude_ai_Gmail__mark_thread_spam
- mcp__claude_ai_Gmail__reply
- mcp__claude_ai_Gmail__search_threads
- mcp__claude_ai_Gmail__send_message
- mcp__claude_ai_Gmail__trash_message
- mcp__claude_ai_Gmail__trash_thread
- mcp__claude_ai_Gmail__unlabel_message
- mcp__claude_ai_Gmail__unlabel_thread
- mcp__claude_ai_Gmail__unmark_message_spam
- mcp__claude_ai_Gmail__unmark_thread_spam
- mcp__claude_ai_Gmail__untrash_message
- mcp__claude_ai_Gmail__untrash_thread
- mcp__claude_ai_Gmail__update_draft
- mcp__claude_ai_Gmail__update_label
- mcp__claude_ai_Gmail__update_message_labels
- mcp__claude_ai_Google_Calendar__create_event
- mcp__claude_ai_Google_Calendar__delete_event
- mcp__claude_ai_Google_Calendar__get_event
- mcp__claude_ai_Google_Calendar__list_calendars
- mcp__claude_ai_Google_Calendar__list_events
- mcp__claude_ai_Google_Calendar__respond_to_event
- mcp__claude_ai_Google_Calendar__search_events
- mcp__claude_ai_Google_Calendar__suggest_time
- mcp__claude_ai_Google_Calendar__update_event
- mcp__claude_ai_Google_Drive__copy_file
- mcp__claude_ai_Google_Drive__create_file
- mcp__claude_ai_Google_Drive__download_file_content
- mcp__claude_ai_Google_Drive__get_file_metadata
- mcp__claude_ai_Google_Drive__get_file_permissions
- mcp__claude_ai_Google_Drive__list_recent_files
- mcp__claude_ai_Google_Drive__read_file_content
- mcp__claude_ai_Google_Drive__search_files
- mcp__claude_ai_Google_Drive__share_file
- mcp__claude_ai_Google_Drive__trash_file
- mcp__claude_ai_Google_Drive__update_file
- mcp__claude_ai_Granola__add_note_to_folder
- mcp__claude_ai_Granola__create_folder
- mcp__claude_ai_Granola__get_account_info
- mcp__claude_ai_Granola__get_meeting_attachment
- mcp__claude_ai_Granola__get_meeting_transcript
- mcp__claude_ai_Granola__get_meetings
- mcp__claude_ai_Granola__give_feedback
- mcp__claude_ai_Granola__list_meeting_folders
- mcp__claude_ai_Granola__list_meetings
- mcp__claude_ai_Granola__query_granola_meetings
- mcp__claude_ai_Granola__remove_note_from_folder
- mcp__claude_ai_Granola__search_meetings
- mcp__claude_ai_Granola__sign_out
- mcp__claude_ai_Granola__update_folder
- mcp__claude_ai_Langmail__archive_emails
- mcp__claude_ai_Langmail__create_calendar
- mcp__claude_ai_Langmail__create_calendar_event
- mcp__claude_ai_Langmail__create_contact
- mcp__claude_ai_Langmail__create_draft
- mcp__claude_ai_Langmail__create_mail_rule
- mcp__claude_ai_Langmail__delete_calendar_event
- mcp__claude_ai_Langmail__delete_contact
- mcp__claude_ai_Langmail__delete_draft
- mcp__claude_ai_Langmail__delete_mail_rule
- mcp__claude_ai_Langmail__download_attachment
- mcp__claude_ai_Langmail__get_draft
- mcp__claude_ai_Langmail__get_email
- mcp__claude_ai_Langmail__get_thread
- mcp__claude_ai_Langmail__list_calendar_events
- mcp__claude_ai_Langmail__list_calendars
- mcp__claude_ai_Langmail__list_drafts
- mcp__claude_ai_Langmail__list_mail_rules
- mcp__claude_ai_Langmail__list_upcoming_birthdays
- mcp__claude_ai_Langmail__mark_emails
- mcp__claude_ai_Langmail__move_calendar_events
- mcp__claude_ai_Langmail__move_emails
- mcp__claude_ai_Langmail__preview_email
- mcp__claude_ai_Langmail__preview_mail_rule
- mcp__claude_ai_Langmail__reply_to_message
- mcp__claude_ai_Langmail__respond_to_event
- mcp__claude_ai_Langmail__search_contacts
- mcp__claude_ai_Langmail__search_emails
- mcp__claude_ai_Langmail__send_draft
- mcp__claude_ai_Langmail__trash_emails
- mcp__claude_ai_Langmail__update_calendar
- mcp__claude_ai_Langmail__update_calendar_event
- mcp__claude_ai_Langmail__update_contact
- mcp__claude_ai_Langmail__update_draft
- mcp__claude_ai_Langmail__update_mail_rule
- mcp__claude_ai_Langmail__upload_attachments
- mcp__claude_ai_Slack__slack_add_list_record
- mcp__claude_ai_Slack__slack_add_reaction
- mcp__claude_ai_Slack__slack_complete_file_upload
- mcp__claude_ai_Slack__slack_create_canvas
- mcp__claude_ai_Slack__slack_create_conversation
- mcp__claude_ai_Slack__slack_create_list
- mcp__claude_ai_Slack__slack_get_file_upload_url
- mcp__claude_ai_Slack__slack_get_reactions
- mcp__claude_ai_Slack__slack_list_channel_members
- mcp__claude_ai_Slack__slack_list_user_channels
- mcp__claude_ai_Slack__slack_read_canvas
- mcp__claude_ai_Slack__slack_read_channel
- mcp__claude_ai_Slack__slack_read_file
- mcp__claude_ai_Slack__slack_read_list
- mcp__claude_ai_Slack__slack_read_thread
- mcp__claude_ai_Slack__slack_read_user_profile
- mcp__claude_ai_Slack__slack_schedule_message
- mcp__claude_ai_Slack__slack_search_channels
- mcp__claude_ai_Slack__slack_search_emojis
- mcp__claude_ai_Slack__slack_search_public
- mcp__claude_ai_Slack__slack_search_public_and_private
- mcp__claude_ai_Slack__slack_search_users
- mcp__claude_ai_Slack__slack_send_message
- mcp__claude_ai_Slack__slack_send_message_draft
- mcp__claude_ai_Slack__slack_update_canvas
- mcp__claude_ai_Slack__slack_update_list
- mcp__claude_ai_Slack__slack_update_list_record
- mcp__claude_ai_betterstack__acknowledge_incident
- mcp__claude_ai_betterstack__add_chart_to_dashboard
- mcp__claude_ai_betterstack__add_dashboard_section
- mcp__claude_ai_betterstack__add_escalation_policy_step_member
- mcp__claude_ai_betterstack__application
- mcp__claude_ai_betterstack__applications
- mcp__claude_ai_betterstack__available_incident_escalation_policies
- mcp__claude_ai_betterstack__catalog_relation
- mcp__claude_ai_betterstack__catalog_relations
- mcp__claude_ai_betterstack__change_team_member_role
- mcp__claude_ai_betterstack__chart
- mcp__claude_ai_betterstack__chart_alert
- mcp__claude_ai_betterstack__chart_alert_help
- mcp__claude_ai_betterstack__chart_alerts
- mcp__claude_ai_betterstack__chart_building_help
- mcp__claude_ai_betterstack__clusters
- mcp__claude_ai_betterstack__create_application
- mcp__claude_ai_betterstack__create_catalog_relation
- mcp__claude_ai_betterstack__create_chart_alert
- mcp__claude_ai_betterstack__create_cloud_connection
- mcp__claude_ai_betterstack__create_collector
- mcp__claude_ai_betterstack__create_dashboard
- mcp__claude_ai_betterstack__create_error_comment
- mcp__claude_ai_betterstack__create_error_issue
- mcp__claude_ai_betterstack__create_heartbeat
- mcp__claude_ai_betterstack__create_incident
- mcp__claude_ai_betterstack__create_incident_comment
- mcp__claude_ai_betterstack__create_metric_expression
- mcp__claude_ai_betterstack__create_monitor
- mcp__claude_ai_betterstack__create_outgoing_webhook
- mcp__claude_ai_betterstack__create_release
- mcp__claude_ai_betterstack__create_source
- mcp__claude_ai_betterstack__create_status_page_report
- mcp__claude_ai_betterstack__create_status_page_report_update
- mcp__claude_ai_betterstack__create_status_page_resource
- mcp__claude_ai_betterstack__create_status_page_section
- mcp__claude_ai_betterstack__dashboard
- mcp__claude_ai_betterstack__dashboard_groups
- mcp__claude_ai_betterstack__dashboard_query_help
- mcp__claude_ai_betterstack__dashboard_templates
- mcp__claude_ai_betterstack__dashboards
- mcp__claude_ai_betterstack__data_regions
- mcp__claude_ai_betterstack__delete_catalog_records
- mcp__claude_ai_betterstack__delete_chart_alert
- mcp__claude_ai_betterstack__delete_metric_expression
- mcp__claude_ai_betterstack__documentation
- mcp__claude_ai_betterstack__edit_application
- mcp__claude_ai_betterstack__edit_chart
- mcp__claude_ai_betterstack__edit_chart_alert
- mcp__claude_ai_betterstack__edit_dashboard
- mcp__claude_ai_betterstack__edit_dashboard_section
- mcp__claude_ai_betterstack__edit_slack_integration
- mcp__claude_ai_betterstack__error
- mcp__claude_ai_betterstack__error_comments
- mcp__claude_ai_betterstack__errors
- mcp__claude_ai_betterstack__errors_query_help
- mcp__claude_ai_betterstack__escalate_incident
- mcp__claude_ai_betterstack__escalation_policies
- mcp__claude_ai_betterstack__escalation_policy
- mcp__claude_ai_betterstack__exploration
- mcp__claude_ai_betterstack__explorations
- mcp__claude_ai_betterstack__explore_logs_query_help
- mcp__claude_ai_betterstack__export_dashboard
- mcp__claude_ai_betterstack__heartbeat
- mcp__claude_ai_betterstack__heartbeat_availability
- mcp__claude_ai_betterstack__heartbeats
- mcp__claude_ai_betterstack__import_dashboard
- mcp__claude_ai_betterstack__incident
- mcp__claude_ai_betterstack__incident_comments
- mcp__claude_ai_betterstack__incident_timeline
- mcp__claude_ai_betterstack__incidents
- mcp__claude_ai_betterstack__invite_team_member
- mcp__claude_ai_betterstack__link_error_issue
- mcp__claude_ai_betterstack__metric
- mcp__claude_ai_betterstack__metric_expressions
- mcp__claude_ai_betterstack__metrics_query_help
- mcp__claude_ai_betterstack__metrics_schema
- mcp__claude_ai_betterstack__monitor
- mcp__claude_ai_betterstack__monitor_availability
- mcp__claude_ai_betterstack__monitor_response_times
- mcp__claude_ai_betterstack__monitors
- mcp__claude_ai_betterstack__move_charts
- mcp__claude_ai_betterstack__on_call
- mcp__claude_ai_betterstack__on_call_event
- mcp__claude_ai_betterstack__on_call_events
- mcp__claude_ai_betterstack__on_call_rotation
- mcp__claude_ai_betterstack__on_calls
- mcp__claude_ai_betterstack__outgoing_webhook
- mcp__claude_ai_betterstack__outgoing_webhooks
- mcp__claude_ai_betterstack__query
- mcp__claude_ai_betterstack__query_help
- mcp__claude_ai_betterstack__query_windows
- mcp__claude_ai_betterstack__releases
- mcp__claude_ai_betterstack__remove_catalog_relation
- mcp__claude_ai_betterstack__remove_chart
- mcp__claude_ai_betterstack__remove_dashboard
- mcp__claude_ai_betterstack__remove_dashboard_section
- mcp__claude_ai_betterstack__remove_dashboard_variable
- mcp__claude_ai_betterstack__remove_escalation_policy_step_member
- mcp__claude_ai_betterstack__remove_exploration_variable
- mcp__claude_ai_betterstack__remove_heartbeat
- mcp__claude_ai_betterstack__remove_incident_comment
- mcp__claude_ai_betterstack__remove_monitor
- mcp__claude_ai_betterstack__remove_outgoing_webhook
- mcp__claude_ai_betterstack__remove_release
- mcp__claude_ai_betterstack__remove_status_page_report
- mcp__claude_ai_betterstack__remove_status_page_report_update
- mcp__claude_ai_betterstack__remove_status_page_resource
- mcp__claude_ai_betterstack__remove_status_page_section
- mcp__claude_ai_betterstack__remove_team_member
- mcp__claude_ai_betterstack__render_chart
- mcp__claude_ai_betterstack__reopen_incident
- mcp__claude_ai_betterstack__replays_query_help
- mcp__claude_ai_betterstack__resolve_incident
- mcp__claude_ai_betterstack__set_dashboard_variable
- mcp__claude_ai_betterstack__set_exploration_variable
- mcp__claude_ai_betterstack__severities
- mcp__claude_ai_betterstack__severity
- mcp__claude_ai_betterstack__slack_integration
- mcp__claude_ai_betterstack__slack_integrations
- mcp__claude_ai_betterstack__source
- mcp__claude_ai_betterstack__source_fields
- mcp__claude_ai_betterstack__sources
- mcp__claude_ai_betterstack__status_page
- mcp__claude_ai_betterstack__status_page_report_update
- mcp__claude_ai_betterstack__status_page_report_updates
- mcp__claude_ai_betterstack__status_page_reports
- mcp__claude_ai_betterstack__status_page_resources
- mcp__claude_ai_betterstack__status_page_sections
- mcp__claude_ai_betterstack__status_pages
- mcp__claude_ai_betterstack__team_members
- mcp__claude_ai_betterstack__team_roles
- mcp__claude_ai_betterstack__teams
- mcp__claude_ai_betterstack__toggle_chart_alert_pause
- mcp__claude_ai_betterstack__unlink_error_issue
- mcp__claude_ai_betterstack__update_catalog_relation
- mcp__claude_ai_betterstack__update_error_state
- mcp__claude_ai_betterstack__update_heartbeat
- mcp__claude_ai_betterstack__update_incident_comment
- mcp__claude_ai_betterstack__update_metric_expression
- mcp__claude_ai_betterstack__update_monitor
- mcp__claude_ai_betterstack__update_outgoing_webhook
- mcp__claude_ai_betterstack__update_status_page
- mcp__claude_ai_betterstack__update_status_page_report
- mcp__claude_ai_betterstack__update_status_page_report_update
- mcp__claude_ai_betterstack__update_status_page_resource
- mcp__claude_ai_betterstack__update_status_page_section
- mcp__claude_ai_betterstack__upsert_catalog_records
- mcp__helpdesk__add_internal_note
- mcp__helpdesk__assign_tickets
- mcp__helpdesk__delete_tickets
- mcp__helpdesk__escalate_tickets
- mcp__helpdesk__forward_ticket
- mcp__helpdesk__get_ticket
- mcp__helpdesk__log_time
- mcp__helpdesk__merge_tickets
- mcp__helpdesk__reply_to_ticket
- mcp__helpdesk__schedule_followup
- mcp__helpdesk__search_tickets
- mcp__helpdesk__set_ticket_status

## Cases

Every case below is a separate conversation. For each, decide the one search you would run first. If you would not need
any tool (for example you would ask the user something first), give neither.

### Case B01

User: let the customer on 4812 know the refund went out today

### Case B02

User: leave a note for Kim Lee on 4812 that finance aproved the refund

### Case B03

User: send 5033 over to their accountant at maria.lopez@lopez-cpa.example

### Case B04

User: 4791 is the same as 4790, get rid of the dupe

### Case B05

User: close out 4655, customer confirmed its working now

### Case B06

User: 5002 is pure spam, kill it

### Case B07

User: give 4888 to Priya

### Case B08

User: 4920 needs tier 2, the webhook payloads are coming thru corrupted and thats beyond us

### Case B09

User: Kim Park should take 5011 personally, she fixed the same bug last month

### Case B10

User: jot down on 4703 that the customer called and was pretty upset

### Case B11

User: update 4844 about the delay

### Case B12

User: set 4950 to pending, waiting on the customer to send logs

### Case C01

User: whats the latest on 4812?

### Case C02

User: delete 5101 and 5102, those are test tickets i made

### Case C03

User: 4730 and 4731 are dupes of 4729, fold them in

### Case C04

User: escalate 4866 to onboarding, they never got there setup call

### Case C05

User: 4801 4802 4803 can all be solved, the outage fix covers them

### Case C06

User: log 20 min on 4999

### Case C07

User: remind me about 5077 in 2 hours

### Case C08

User: reply on 4840: we've reissued the invoice, should be in your inbox in a few minutes

### Case C09

User: fwd 4915 to legal@wayne-logistics.example

### Case C10

User: assign 4760 and 4761 to Jon Reyes

### Case O01

User: email the customer on 4812 that the refund went out today, should hit their card in 3-5 business days

### Case O02

User: escalate 4920 to Tier 2 pls, their API keys keep failing auth, not a billing thing

### Case O03

User: remind me tuesday 10am to check 4701 again, waiting on their bank

### Case O04

User: forward 5033 to their accountant, m.huber@huber-steuer.example, she needs the invoice dispute details

### Case O05

User: leave a comment for Kim Lee on 4812: don't refund again, I already did it in Stripe

### Case O06

User: 4655 is resolved, customer confirmed the card goes through now, close it out

### Case O07

User: put 4733 on Priya's plate, she's covering billing on-call tonight

### Case O08

User: log 45 min on 4890 for the call I just had with them

### Case O09

User: customer emailed twice, 4806 is a dupe of 4801, fold it into 4801

### Case O10

User: trash 4999, it's bot spam, no real customer

### Case O11

User: reply on Kim's thread about 4812 saying the refund is processed

### Case O12

User: 5102, the outage one, mark it resolved and add a comment that the fix is deployed
