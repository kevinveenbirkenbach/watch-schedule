# Watch-Schedule

Crafted by Kevin Veen-Birkenbach ([kevin@veen.world](mailto:kevin@veen.world), [veen.world](https://www.veen.world)), this software enables efficient watch scheduling for the SY-Amy2's voyage from Alicante to Korfu. Journey specifics can be accessed [here](https://www.sy-amy2.de/?p=64). Interestingly, it was developed amidst relatively calm seas, with waves less than 1.5m high, as we sailed and motored north of Alicante.

The software creates a sailing shift schedule, automatically pairing an experienced sailor with a novice sailor for each 3.5-hour shift. It provides timestamps in UTC, WEST, and CEST, and saves the final schedule in a CSV file for convenient viewing and usage. 

## Development
This project was developed with the assistance of Chat GPT from OpenAI. The conversation leading to the development of this software can be found [here](https://chat.openai.com/share/94c6eec2-6057-4a3a-a88d-c5a8cd18d883).

## Configuration Parameters

In order to use this application, you need to provide a configuration file in JSON format with specific parameters. Below is the description of each parameter:

### crew
The `crew` parameter is an array of crew members. Each crew member is represented by a dictionary containing the following keys:
* `name`: The name of the crew member.
* `experience`: A number representing the experience level of the crew member. Higher numbers represent more experience.
* `watch_count`: A number representing the number of watches the crew member has had. This count will be updated as the shift plan is created.
* `alert_time`: The alert_time parameter (inside each crew member dictionary) is a number representing the number of seconds before the shift starts that an alert should be triggered. This alert will be included in the .ics file for each crew member, and will go off at the specified time before the start of each shift.

Note: Alerts rely on the calendar software that the .ics file is imported into to support and enable alerts. Not all calendar software will support this feature.

### start_date
The `start_date` parameter is a string representing the starting date and time of the shifts in the format `YYYY-MM-DD HH:MM`.

### end_date
The `end_date` parameter is a string representing the ending date and time of the shifts in the format `YYYY-MM-DD HH:MM`.

### shiftduration
The `shiftduration` parameter is a string representing the duration of each shift in the format `HH:MM`.

### description
The `description` parameter is a string providing a link or details about the specific shift plan.

### depature_location
The `depature_location` parameter is a string indicating the starting location of the shift.

### arrival_location
The `arrival_location` parameter is a string indicating the ending location of the shift.

### ship_name
The `ship_name` parameter is a string representing the name of the ship for which the shift plan is being created.

## Usage

To use these parameters, fill in the JSON file (for instance, `description.json`) as per your requirements and then run the script using this file as an input. 

For instance:

```json
{
    "crew": [
        {"name":"Dirk","experience":"10","watch_count":0, "alert_time": 600},
        {"name":"Thomas","experience":"8","watch_count":0, "alert_time": 600},
        {"name":"Kevin","experience":"8","watch_count":0, "alert_time": 600},
        {"name":"Detlef","experience":"6","watch_count":0, "alert_time": 600},
        {"name":"Steve","experience":"2","watch_count":0, "alert_time": 1200},
        {"name":"Lasse","experience":"4","watch_count":0, "alert_time": 600},
        {"name":"Stefan","experience":"5","watch_count":0, "alert_time": 900}
    ],
    "start_date":"2023-07-15 14:00",
    "end_date":"2023-07-26 22:00",
    "shiftduration":"03:30",
    "description":"The turn description can be found here: https://www.sy-amy2.de/?p=64",
    "depature_location":"Alicante",
    "arrival_location":"Brest",
    "ship_name":"SY-Amy2"
}
```

Run the script with the command:

```bash
python shift_planner.py
```

After successful execution, you will find your crew shift plan in a CSV file named `shift_plan.csv` and individual `.ics` calendar files for each crew member.


## License
This project is licensed under the terms of the GNU Affero General Public License v3.0. You can find a copy of the license in the LICENSE file or at [GNU Licenses](https://www.gnu.org/licenses/).
