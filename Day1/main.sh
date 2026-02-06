#!/bin/bash

logfile="logfile.txt"
echo ""
timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
HOSTNAME=$(hostname)
EMAIL_TO="venuvikas175@gmail.com"
REPORT="/tmp/system_report.txt"

echo "$timestamp"

function check_disk_usage() {
    echo -e "\nChecking disk usage..."
    df -h
    echo ""
}

function monitor_running_services() {
    echo -e "\nMonitoring running services..."
    systemctl list-units --type=service --state=running
    echo -e "\n"
}

function assess_memory_usage() {
    echo -e "\nAssessing memory usage..."
    free -h
    echo -e "\n"
}

function evaluate_cpu_usage() {
    echo -e "\nEvaluating usage of CPU..."
    top -bn1
    echo -e "\n"
}

function send_email_report() {
    echo -e "\nGenarating and sending report via Email..."
     {
        echo "System Report"
        echo "Host: $HOSTNAME"
        echo "Date: $timestamp"
        echo "=================================="
        echo
        echo "Disk Usage:"
        df -h
        echo
        echo "Memory Usage:"
        free -h
        echo
        echo "CPU Usage:"
        top -bn1 | head -15
        echo
        echo "Running Services:"
        systemctl list-units --type=service --state=running
    } > "$REPORT"

    mail -s "System Report - $HOSTNAME" "$EMAIL_TO" < "$REPORT"

    echo "Email sent successfully."
    echo -e "\n"
}

while true; do
  echo -e "\n1) Check Disk Usage" # Check for space errors
  echo "2) Monitor Running Services"
  echo "3) Assess Memory Usage"
  echo "4) Evaluate CPU Usage"
  echo "5) Send a Comprehensive Report via Email Every Four Hours"
  echo -e "6) Exit\n"

  read -p "Please select an option between [1-6]: " choice

  case "$choice" in

    1) 
     check_disk_usage
     break;;

    2) 
     monitor_running_services
     break;;

    3) 
     assess_memory_usage
     break;; 

    4) 
     evaluate_cpu_usage
     break;;   

    5) 
     send_email_report
     break;;

    6)
     echo "Exiting..."
     exit 0;;

    *)
     echo "Invalid input. Please enter a numerical between 1 to 6"     
     ;;

  esac
done;