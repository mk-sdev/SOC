import click, json, os

def alert_viewer(alerts):
    '''
    Interactive alert viewer    
    '''
    i = 0
    message = ""
    color = ""
    while True:
        os.system("clear")

        # print the log
        click.echo(json.dumps(alerts[i], indent=2))

        if message:
            click.secho(f"\n{message}", fg=color)
        message = ""

        # print available options
        click.secho(
            "\n[c,o,m,p,n,f,t,g,q,h]", fg="blue"
        )

        choice = input()

        if choice == 'c':
            alerts[i]["closed"] = True
            message= "Alert marked as closed"; color="green"
        elif choice == 'o':
            if "closed" in alerts[i]:
                del alerts[i]["closed"]
        elif choice == 'm':
            comment = input("Enter your comment: ")
            alerts[i]["comment"] = comment
            if comment == "":
                del alerts[i]["comment"]
            else:
                message= "Comment added"; color="green"
        elif choice == 'p':
            if i == 0:
                message = "Can't display the previous alert"; color="red"
            else:
                i = i - 1;
        elif choice == 'n':
            if i == len(alerts) - 1:
                message = "Can't display the next alert"; color="red"
            else:
                i = i + 1
        elif choice == 'f':
            alerts[i]["closed"] = True
            alerts[i]["false_positive"] = True
            message= "Alert marked as false positive and closed"; color="green"
        elif choice == 't':
            if "closed" in alerts[i] and "false_positive" in alerts[i]:
                del alerts[i]["closed"]
                del alerts[i]["false_positive"]
        elif choice == 'g':
            id = int(input("Give the id of an alert you want to go to: "))
            index = next((index for index, log in enumerate(alerts) if log["id"] == id), None)

            if index is not None:
                i = index
            else:
                message = "Alert of a given id doesn't exist in the set"; color = 'red'
        elif choice == 'q':
            break
        elif choice == 'h':
            message = "c - close\to - open\tm - comment\tp - previous\tn - next\tf - mark as false positive and close\tt - mark as true positive\tg - go to\tq - quit\th - display help"; color="blue"
        else: message='Unknown option; type h for help'; color = 'red'
        
        # Updating a log in the JSON file
        update_log_in_file(alerts[i])


def update_log_in_file(updated_log):
    log_path = "/logs/alerts.json"

    with open(log_path, "r") as f:
        alerts = json.load(f)

    # update 
    for i, alert in enumerate(alerts):
        if alert["id"] == updated_log["id"]:
            alerts[i] = updated_log
            break

    # save (rewrites only one log)
    with open(log_path, "w") as f:
        json.dump(alerts, f)


