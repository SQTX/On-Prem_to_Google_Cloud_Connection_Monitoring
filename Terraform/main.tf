resource "google_monitoring_notification_channel" "email_channel" {
  display_name = "Email Notification Channel"
  type         = "email"

  labels = {
    email_address = var.email_address
  }
}

resource "google_monitoring_alert_policy" "user_router_alert_policy" {
  display_name = "User-Router Alert Policy"

  conditions {
    display_name = "User-Router Condition"

    condition_matched_log {
      filter = "logName=\"${var.log_name}\" AND jsonPayload.level_failed=3"
    }
  }

  combiner = "OR"

  notification_channels = [
    google_monitoring_notification_channel.email_channel.name,
  ]

  documentation {
    content  = "Policy triggers when at least one log matching the filter appears."
    mime_type = "text/markdown"
  }

  user_labels = {
    severity = "warning"
  }

  alert_strategy {
    notification_rate_limit {
      period = "3600s"  # One notification per hour
    }
    auto_close = "604800s"  # 7 days in seconds
  }
  severity = "WARNING"
}

resource "google_monitoring_alert_policy" "user_dns_alert_policy" {
  display_name = "User-DNS Alert Policy"
  combiner     = "OR"
  notification_channels = [
    google_monitoring_notification_channel.email_channel.name,
  ]

  conditions {
    display_name = "User-DNS Condition"

    condition_matched_log {
      filter = "logName=\"${var.log_name}\" AND jsonPayload.level_failed=2"
    }
  }

  documentation {
    content  = "Policy triggers when at least one log matching the filter appears."
    mime_type = "text/markdown"
  }

  user_labels = {
    severity = "warning"
  }

  alert_strategy {
    notification_rate_limit {
      period = "3600s"
    }
    auto_close = "604800s"
  }

  severity = "WARNING"
}

resource "google_monitoring_alert_policy" "user_vm_connection_alert_policy" {
  display_name = "User-VM Connection Alert Policy"
  combiner     = "OR"
  notification_channels = [
    google_monitoring_notification_channel.email_channel.name,
  ]

  conditions {
    display_name = "User-VM Connection Condition"

    condition_matched_log {
      filter = "logName=\"${var.log_name}\" AND jsonPayload.level_failed=1"
    }
  }

  documentation {
    content  = "Policy triggers when at least one log matching the filter appears."
    mime_type = "text/markdown"
  }

  user_labels = {
    severity = "warning"
  }

  alert_strategy {
    notification_rate_limit {
      period = "3600s"
    }
    auto_close = "604800s"
  }

  severity = "WARNING"
}

resource "google_monitoring_alert_policy" "user_isp_connection_alert_policy" {
  display_name = "User-ISP Connection Alert Policy"
  combiner     = "OR"
  notification_channels = [
    google_monitoring_notification_channel.email_channel.name,
  ]

  conditions {
    display_name = "User-VM Connection Condition"

    condition_matched_log {
      filter = "logName=\"${var.log_name}\" AND jsonPayload.level_failed=4"
    }
  }

  documentation {
    content  = "Policy triggers when at least one log matching the filter appears."
    mime_type = "text/markdown"
  }

  user_labels = {
    severity = "warning"
  }

  alert_strategy {
    notification_rate_limit {
      period = "3600s"
    }
    auto_close = "604800s"
  }

  severity = "WARNING"
}
