# Astro UXDS Mock Data

Generate "contacts", "alerts" and "mnemonics" data for testing Astro Web Components and building demo applications.

## Install

```bash
npm install @astrouxds/mock-data
```

## Getting Started

The example below creates a state object with the generated contacts and maps the alerts and mnemonics connected to those contacts on their respective properties.

```ts
import { generateContacts } from '@astrouxds/mock-data';

const contacts = generateContacts();

const state = {
  contacts,
  alerts: contacts.flatMap(({ alerts }) => alerts),
  mnemonics: contacts.flatMap(({ mnemonics }) => mnemonics),
};

console.log(state);
```

## Contacts

Contacts include alerts with a "contact ref" on the alert based on where in the array (the index) a contact is. Meaning not all contacts will have alerts, only a percentage of them will.

All contacts will have mnemonics as an array property on the contact object.

```ts
import { generateContacts } from '@astrouxds/mock-data';
```

```ts
const contacts = generateContacts(); // returns 100 contacts by default
```

```ts
const contacts = generateContacts(300); // returns 300 contacts
```

```ts
// returns 200 contacts with options provided below
const contacts = generateContacts(200, {
  alertsPercentage: 5, // percentage of the 200 contacts to have an alert @default 10%
  secondAlertPercentage: 3, // percentage of the 200 contacts to have 2 alerts @default 2%
  daysRange: 2, // range of the start and end timestamps @default 1 day
  dateRef: '3/17/2008', // date reference for timestamps @default now
});
```

## Alerts

If you just want alerts without any contact ref you can generate just an array of alerts.

```ts
import { generateAlerts } from '@astrouxds/mock-data';
```

```ts
const alerts = generateAlerts(5); // returns 5 alerts
```

## Mnemonics

If you just want mnemonics without any contact ref you can generate just an array of alerts.

```ts
import { generateMnemonics } from '@astrouxds/mock-data';
```

```ts
const mnemonics = generateMnemonics(5); // returns 5 mnemonics
```

## Contacts Subscriber

Publishes 100 contacts and generates a new contact every 5 seconds up to 200 contacts by default.

```ts
import { onContactsChange } from '@astrouxds/mock-data';
```

```ts
const unsubscribe = onContactsChange((contacts) => {
  console.log(contacts);
});
```

With options as second argument

```ts
const unsubscribe = onContactsChange(
  (contacts) => console.log(contacts),
  { limit: 50 }, // options with a limit of 50
);
```

Use the unsubscribe function returned from onContactsChange to unsubscribe

```ts
setTimeout(() => {
  unsubscribe();
}, 1000 * 60 * 5); // unsubscribe after 5 mins
```

## Contacts Subscriber Example With React

```ts
import { useEffect, useState } from 'react';
import { onContactsChange, Contact } from '@astrouxds/mock-data';

const App = () => {
  const [contacts, setContacts] = useState<Contact[]>([]);

  useEffect(() => {
    const unsubscribe = onContactsChange((contacts) => {
      setContacts(contacts);
    });

    return () => {
      unsubscribe();
    };
  }, []);

  return (
    <ul>
      {contacts.map(({ id, equipment }) => (
        <li key={id}>{equipment}</li>
      ))}
    </ul>
  );
};

export default App;
```

## Contacts Service

Class based store for instaciating then subscribing to an auto-generate contacts state

```ts
import { ContactsService } from '@astrouxds/mock-data';

// with manually set options
const contactsService = new ContactsService({
  initial: 10,
  interval: 2,
  limit: 20,
});

let contacts: Contact[] = [];
const unsubscribe = contactsService.subscribe((data) => {
  contacts = data;
});
```

Use the unsubscribe function returned from contactsService.subscribe to unsubscribe

```ts
setTimeout(() => {
  unsubscribe();
}, 1000 * 60 * 5); // unsubscribe after 5 mins
```

<!-- ## Contacts Service Example With React

```ts
import { useSyncExternalStore } from 'react';
import { ContactsService } from '@astrouxds/mock-data';

const contactsService = new ContactsService({
  initial: 10,
  interval: 2,
  limit: 20,
});

const App = () => {
  const contactsData = useSyncExternalStore(
    contactService.subscribe,
    contactsService.getContacts,
  );

  const { contacts } = contactService.selectContacts(contactsData);

  return (
    <ul>
      {contacts.map(({ id, equipment }) => (
        <li key={id}>{equipment}</li>
      ))}
    </ul>
  );
};

export default App;
```

- The useSyncExternalStore hook takes two arguments (subscribe function, getSnapshot function) and one optional argument (getServerSnapshot function). The getServerSnapshot function is not supported and therefore SSR is not supported at this time. -->

## API

###### `function`

### generateContacts

Returns an array of contacts.

#### Parameters

| Name                          | Type                             | Default | Description                                                                |
| ----------------------------- | -------------------------------- | ------- | -------------------------------------------------------------------------- |
| length                        | number                           | 100     | The total number of contacts to generate.                                  |
| options                       | {...}                            | {}      | If no options are set, the defaults are used as described below.           |
| options.alertsPercentage      | AlertsPercentage                 | 10      | The percentage of contacts which should have an alert connected to them.   |
| options.secondAlertPercentage | AlertsPercentage                 | 2       | The percentage of contacts which should have two alerts connected to them. |
| options.daysRange             | number                           | 1       | The range in days for the span between the start and end timestamps.       |
| options.dateRef               | string &#124; number &#124; Date | now     | The date to reference when generating the contacts.                        |

###### `function`

### generateContact

Returns a single contact.

#### Parameters

| Name    | Type   | Default  | Description                                                             |
| ------- | ------ | -------- | ----------------------------------------------------------------------- |
| index   | number | required | The index is used to determine if an alert(s) is connected the contact. |
| options | {...}  | {}       | The same options from <b>generateContacts</b>                           |

###### `function`

### generateAlerts

Returns an array of alerts.

#### Parameters

| Name                 | Type                             | Default   | Description                                                                                                      |
| -------------------- | -------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------- |
| length               | number                           | 40        | The total number of alerts to generate.                                                                          |
| options              | {...}                            | {}        | If no options are set, the defaults are used as described below.                                                 |
| options.contactRefId | string                           | ''        | A contact reference id. Will be an empty string if not provided.                                                 |
| options.equipment    | string                           | undefined | An equipment config string. Will be generated if not provided.                                                   |
| options.createdRef   | string &#124; number &#124; Date | undefined | The date to reference when generating the alerts. If provided, this will override any start and end options set. |
| options.start        | string &#124; number &#124; Date | undefined | The starting timestamp for the alert timestamp boundry.                                                          |
| options.end          | string &#124; number &#124; Date | undefined | The ending timestamp for the alert timestamp boundry.                                                            |

###### `function`

### generateAlert

Returns a single alert.

#### Parameters

| Name    | Type  | Default | Description                                 |
| ------- | ----- | ------- | ------------------------------------------- |
| options | {...} | {}      | The same options from <b>generateAlerts</b> |

### generateMnemonics

Returns an array of menmonics.

#### Parameters

| Name                 | Type   | Default | Description                                                                                              |
| -------------------- | ------ | ------- | -------------------------------------------------------------------------------------------------------- |
| length               | number | 9       | The total number of alerts to generate.                                                                  |
| options              | {...}  | {}      | If no options are set, the defaults are used as described below.                                         |
| options.contactRefId | string | ''      | A contact reference id. Will be an empty string if not provided.                                         |
| options.thresholdMin | number | 0       | The minimum threshold for the mnemonic value.                                                            |
| options.thresholdMax | number | 110     | The maximum threshold for the mnemonic value.                                                            |
| options.deviation    | number | 20      | The amount the mnemonic value is allow to exceed the threshold maximum or subceed the threshold minimum. |
| options.precision    | number | 0.1     | The number of decimal places the mnemonic value will include.                                            |

###### `function`

### generateMnemonic

Returns a single mnemonic.

#### Parameters

| Name    | Type  | Default | Description                                    |
| ------- | ----- | ------- | ---------------------------------------------- |
| options | {...} | {}      | The same options from <b>generateMnemonics</b> |

###### `function`

### onContactsChange

Publishes 100 contacts and generates a new contact every 5 seconds up to 200 contacts by default.

Returns an unsubscribe function.

#### Parameters

| Name                          | Type                             | Default  | Description                                                                |
| ----------------------------- | -------------------------------- | -------- | -------------------------------------------------------------------------- |
| callback                      | (contacts: Contact[]) => void    | required | A callback function which receives the latest contacts array.              |
| options                       | OnContactChangeOptions           | {}       | If no options are set, the defaults are used as described below.           |
| options.alertsPercentage      | AlertsPercentage                 | 10       | The percentage of contacts which should have an alert connected to them.   |
| options.secondAlertPercentage | AlertsPercentage                 | 2        | The percentage of contacts which should have two alerts connected to them. |
| options.daysRange             | number                           | 1        | The range in days for the span between the start and end timestamps.       |
| options.dateRef               | string &#124; number &#124; Date | now      | The date to reference when generating the contacts.                        |
| options.initial               | number                           | 100      | The initial number of contacts generated on subscribe.                     |
| options.interval              | number                           | 5        | The interval in seconds which new contacts are generated and published.    |
| options.limit                 | number                           | 200      | The limit of new contacts to generate and publish.                         |

###### `class`

### ContactsService

Generates initial contacts, publishes a new contact every x amount of seconds, and has methods to add, update, and delete a contact.

Returns an instance a ContactsService.

##### Parameters

| Name                          | Type                             | Default | Description                                                                |
| ----------------------------- | -------------------------------- | ------- | -------------------------------------------------------------------------- |
| options                       | ContactsServiceOptions           | {}      | If no options are set, the defaults are used as described below.           |
| options.alertsPercentage      | AlertsPercentage                 | 10      | The percentage of contacts which should have an alert connected to them.   |
| options.secondAlertPercentage | AlertsPercentage                 | 2       | The percentage of contacts which should have two alerts connected to them. |
| options.daysRange             | number                           | 1       | The range in days for the span between the start and end timestamps.       |
| options.dateRef               | string &#124; number &#124; Date | now     | The date to reference when generating the contacts.                        |
| options.initial               | number                           | 100     | The initial number of contacts generated on subscribe.                     |
| options.interval              | number                           | 5       | The interval in seconds which new contacts are generated and published.    |
| options.limit                 | number                           | 200     | The limit of new contacts to generate and publish.                         |

#### Methods

`subscribe`

Subscribes to received published contacts.

Returns a function to unsubscribe.

##### Parameters

| Name     | Type                          | Default  | Description                                                   |
| -------- | ----------------------------- | -------- | ------------------------------------------------------------- |
| callback | (contacts: Contact[]) => void | required | A callback function which receives the latest contacts array. |

`addContact`

Adds a newly generated contact.

Returns the added contact.

##### Parameters

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
|      |      |         |             |

`updateContact`

Updates the specified contact.

Returns a success message.

##### Parameters

| Name                    | Type                    | Default   | Description                      |
| ----------------------- | ----------------------- | --------- | -------------------------------- |
| id                      | uuid                    | required  | The id of the contact to modify. |
| params                  | UpdateContactParams     | {}        | An optional params object.       |
| params.ground           | ContactGround           | undefined | Optional property to modify.     |
| params.satellite        | string                  | undefined | Optional property to modify.     |
| params.equipment        | string                  | undefined | Optional property to modify.     |
| params.state            | ContactState            | undefined | Optional property to modify.     |
| params.step             | ContactStep             | undefined | Optional property to modify.     |
| params.detail           | string                  | undefined | Optional property to modify.     |
| params.beginTimestamp   | number                  | undefined | Optional property to modify.     |
| params.endTimestamp     | number                  | undefined | Optional property to modify.     |
| params.resolution       | ContactResolution       | undefined | Optional property to modify.     |
| params.resolutionStatus | ContactResolutionStatus | undefined | Optional property to modify.     |

`deleteContact`

Deletes the specified contact.

Returns a success message.

##### Parameters

| Name | Type | Default  | Description                      |
| ---- | ---- | -------- | -------------------------------- |
| id   | uuid | required | The id of the contact to delete. |

## Schema

### Types

| Type                    | Description                                                                                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AlertCategory           | 'software' &#124; 'spacecraft' &#124; 'hardware'                                                                                                                    |
| AlertsPercentage        | 0 &#124; 2 &#124; 3 &#124; 4 &#124; 5 &#124; 10 &#124; 12 &#124; 15 &#124; 20 &#124; 25 &#124; 34 &#124; 50                                                         |
| ContactGround           | 'CTS' &#124; 'DGS' &#124; 'GTS' &#124; 'TCS' &#124; 'VTS' &#124; 'NHS' &#124; 'TTS' &#124; 'HTS'                                                                    |
| ContactState            | 'executing' &#124; 'failed' &#124; 'ready' &#124; 'updating'                                                                                                        |
| ContactStep             | 'AOS' &#124; 'Command' &#124; 'Configure Operation' &#124; 'Critical Health' &#124; 'DCC' &#124; 'Downlink' &#124; 'Lock' &#124; 'LOS' &#124; 'SARM'&#124; 'Uplink' |
| ContactResolution       | 'complete' &#124; 'failed' &#124; 'pass' &#124; 'prepass' &#124; 'scheduled'                                                                                        |
| ContactResolutionStatus | 'normal' &#124; 'critical' &#124; 'off' &#124; 'standby'                                                                                                            |
| DataType                | 'contact' &#124; 'alert' &#124; 'mnemonic'                                                                                                                          |
| Status                  | 'caution' &#124; 'critical' &#124; 'normal' &#124; 'off' &#124; 'serious' &#124; 'standby'                                                                          |

### Contact

| Property         | Type                    | Description            |
| ---------------- | ----------------------- | ---------------------- |
| id               | string                  | uuid                   |
| type             | DataType                |                        |
| status           | Status                  |                        |
| name             | number                  |                        |
| ground           | ContactGround           |                        |
| rev              | number                  |                        |
| satellite        | string                  |                        |
| equipment        | string                  |                        |
| state            | ContactState            |                        |
| step             | ContactStep             |                        |
| detail           | string                  |                        |
| beginTimestamp   | number                  |                        |
| endTimestamp     | number                  |                        |
| aos              | number                  |                        |
| los              | number                  |                        |
| latitude         | number                  |                        |
| longitude        | number                  |                        |
| azimuth          | number                  |                        |
| elevation        | number                  |                        |
| resolution       | ContactResolution       |                        |
| resolutionStatus | ContactResolutionStatus |                        |
| alerts           | Alert[]                 | An array of alerts.    |
| mnemonics        | Mnemonic[]              | An array of mnemonics. |

### Alert

| Property     | Type          | Description    |
| ------------ | ------------- | -------------- |
| id           | string        | uuid           |
| status       | Status        |                |
| category     | AlertCategory |                |
| message      | string        |                |
| longMessage  | string        |                |
| timestamp    | number        |                |
| selected     | boolean       |                |
| new          | boolean       |                |
| expanded     | boolean       |                |
| acknowledged | boolean       |                |
| contactRefId | string        | uuid &#124; '' |

### Mnemonic

| Property       | Type   | Description    |
| -------------- | ------ | -------------- |
| id             | string | uuid           |
| mnemonicId     | string |                |
| status         | Status |                |
| unit           | string |                |
| thresholdMax   | number |                |
| thresholdMin   | number |                |
| currentValue   | number |                |
| subsystem      | string |                |
| childSubsystem | string |                |
| measurement    | string |                |
| contactRefId   | string | uuid &#124; '' |
