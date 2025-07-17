# Epicollect5 API

## Epicollect5 API

Epicollect5 is currently a **read-only** API. Only **GET** requests are exposed to third party clients/apps.

Adding/editing resources can be done only via Epicollect5 official applications (Android, iOS, web).

Only secure **https** requests are allowed.

## Server responses:

* 200 `OK` the request was successful.
* 400 `Bad Request` the request could not be understood or was missing required parameters.
* 404 `Not Found` the resource was not found.
* 500 `Internal Server Error` something unexpected happened

## Status code responses

When an error occurs, you will receive a status code in the response.

Error objects are returned in the standard [JSON API format](http://jsonapi.org/examples/#error-objects) and consist of:

* code - the EC5 code
* title - a title for the EC5 code (in English)
* source - the source of the response

A full list of the available status codes can be found [here](https://five.epicollect.net/json/ec5-status-codes/en.json).

## Rate limiting

We currently limit access to the API to

* 60 requests per minute for entries.
* 30 requests per minute for media files.
* 1000 entries per request.
* 10 auth tokens per hour.

These limits apply to a single IP address.

{% hint style="warning" %}
Every day, hundreds of developers make requests to the Epicollect5 API. To help manage the sheer volume of these requests, limits are placed on the number of requests that can be made. These limits help us provide a reliable and scalable API that our developer community relies on.
{% endhint %}

## Authentication

For **PRIVATE** projects, access to data is restricted.

To access the data, you need to create an Epicollect5 Client App and generate an API Token, which can be added to all requests made via the **Authorization** header, like so:

`Authorization: Bearer {api_token}`

This can be done from the Project Details page by the **Creator or Manager** of a Project.
# Get Entries

Get the entries for a particular Form for a Project, mapped using either your custom mapping or the EC5 AUTO mapping. If the project is private, an `access_token` must be provided (See: API Authentication).

We assume the base domain to be **five.epicollect.net**.

## HTTP REQUEST

`GET /api/export/entries/{project_slug}?{key=value&key=value...}`

## Query Parameters

| Parameter         | Required            | Description                                                                                                                          |
| ----------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| project\_slug     | yes, as url segment | The slugified project name.                                                                                                          |
| form\_ref         | no                  | The ref used to identify a form. If this is not supplied, the first form form\_ref will be used by default.                          |
| uuid              | no                  | The unique identifier for a particular entry.                                                                                        |
| parent\_form\_ref | no                  | The form ref of a child form's parent.                                                                                               |
| parent\_uuid      | no                  | The uuid of a child entry's parent.                                                                                                  |
| map\_index        | no                  | The integer index of the particular mapping you want the data to be mapped against. The default mapping is used if none is supplied. |
| per\_page         | no                  | The number of entries to show per page. (integer, max 1000). Default is 50.                                                          |
| page              | no                  | The current page. (integer)                                                                                                          |
| sort\_by          | no                  | The column on which to sort.                                                                                                         |
| sort\_order       | no                  | The sort order for the entries: ASC (ascending) or DESC (descending).                                                                |
| filter\_by        | no                  | The column on which to filter.                                                                                                       |
| filter\_from      | no                  | The value to filter from.                                                                                                            |
| filter\_to        | no                  | The value to filter to.                                                                                                              |
| format            | no                  | Get the data in csv format                                                                                                           |
| headers           | no                  | Whether you need the csv headers.                                                                                                    |
| title             | no                  | A title to filter on ([**What is a title?**](https://docs.epicollect.net/formbuilder/title))                                         |

## Further Descriptions

### `project_slug`

The **project\_slug** is slugified version of the project name. Any spaces in the project name are replaced by a hyphen "-" to make it url safe. To retrieve it, check the **Developers** section on your project details page. From the same page you can download the full project definition in JSON format. It is used as a segment in the request url.

### `form_ref`

The **form\_ref** is a unique identifier assigned to each form. To retrieve it, check the **Developers** section on your project details page. From the same page you can download the full project definition in JSON format.

### `uuid`

The **uuid** is a unique identifier for an entry. To retrieve a uuid, check the `id` or `entry_uuid` attribute of an entry object.

### `parent_form_ref`

The **parent\_form\_ref** is the form ref of a parent form to which a child form is related. To retrieve it, check the **Developers** section on your project details page. From the same page you can download the full project definition in JSON format.

### `parent_uuid`

The **parent\_uuid** is a unique identifier for an entry to which a child or children entries are related. For example, if I have a University form entry "Imperial College", it may have 0, 1 or more Department form entries related to it, such as "DIDE", "Biology" etc and each of these child form entries will be related back to the parent entry via the **parent\_uuid**.

To retrieve this, check the `parent`.`data`.`parent_uuid` attribute of an entry object.

### `format`

Accepted values are `csv` or `json`. The default, if none is supplied, is `json`.

### `headers`

Whether to include headers when the format is `csv`. Accepted values are `true` or `false`. The default, if none is supplied, is `true`.

### Sorting

You can currently sort by the columns `created_at` and `uploaded_at` by "ASC" (ascending) or "DESC" (descending) order.

### Filtering

You can currently filter by the columns `created_at` and `uploaded_at`.\
You may choose a DATE value (in ISO 8601 format, like _2022-01-26T00:00:00.000_) on which to filter: "`filter_from`" (all the entries from a value), "`filter_to`" (all the values to a value) or "`filter_from`" and "`filter_to`" (all the entries between two values).

### Title

You can filter entries by their titles passing a search string.
# Get Branch Entries

Get the branch entries for a particular Branch in a Form for a Project, mapped using either your custom mapping or the EC5 AUTO mapping. If the project is private, an `access_token` must be provided (See: API Authentication).

We assume the base domain to be **five.epicollect.net**.

## HTTP REQUEST

`GET /api/export/entries/{project_slug}?{key=value&key=value...}`

## Query Parameters

| Parameter           | Required            | Description                                                                                                                  |
| ------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| project\_slug       | yes, as url segment | The slugified project name.                                                                                                  |
| branch\_ref         | yes                 | The ref of a branch input in a form.                                                                                         |
| branch\_owner\_uuid | no                  | The uuid of the entry which owns the branch entry/entries.                                                                   |
| form\_ref           | no                  | The ref used to identify a form. If this is not supplied, the first form form\_ref will be used by default.                  |
| uuid                | no                  | The unique identifier for a particular branch entry.                                                                         |
| map\_index          | no                  | The index of the particular mapping you want the data to be mapped against. The default mapping is used if none is supplied. |
| per\_page           | no                  | The number of entries to show per page. (max 1000).Default is 50.                                                            |
| page                | no                  | The current page.                                                                                                            |
| format              | no                  | The format of the exported data.                                                                                             |
| headers             | no                  | Whether to include headers or not.                                                                                           |
| sort\_by            | no                  | The column on which to sort.                                                                                                 |
| sort\_order         | no                  | The sort order for the entries: ASC (ascending) or DESC (descending).                                                        |
| filter\_by          | no                  | The column on which to filter.                                                                                               |
| filter\_from        | no                  | The value to filter from.                                                                                                    |
| filter\_to          | no                  | The value to filter to.                                                                                                      |

## Further Descriptions

### `project_slug`

The **project\_slug** is slugified version of the project name. Any spaces in the project name are replaced by a hyphen "-" to make it URL safe. To retrieve it, check the **Developers** section on your project details page. From the same page, you can download the full project definition in JSON format. It is used as a segment in the request URL.

### `branch_ref`

The **branch\_ref** is the reference of the branch input question attached to a form. To retrieve it, check the **Developers** section on your project details page. From the same page you can download the full project definition in JSON format.

Supplying this will return all entries for a particular branch input, regardless of the main entry to which each branch entry is associated.

### `branch_owner_uuid`

The **branch\_owner\_uuid** is a unique identifier for an entry to which a branch entry/entries are associated. For example, if I have a Person form entry "Mr Doe", it may have 0, 1 or more Family Members branch entries associated with it, such as "Mrs Doe", "Miss Doe" etc and each of these branch form entries will be associated back to the main entry via the branch\_owner\_uuid.

Supplying this, along with the **branch\_ref**, will return all entries for a particular branch input for a particular main entry.

To retrieve this, check the `branch`.`data`.`branch_owner_uuid` attribute of a branch entry object.

### `form_ref`

The **form\_ref** is a unique identifier assigned to each form. To retrieve it, check the **Developers** section on your project details page. From the same page you can download the full project definition in JSON format.

### `uuid`

The **uuid** is a unique identifier for a branch entry. To retrieve a uuid, check the `id` or `entry_uuid` attribute of a branch entry object.

### `format`

Accepted values are `csv` or `json`. The default, if none is supplied, is `json`.

### `headers`

Whether to include headers when the format is `csv`. Accepted values are `true` or `false`. The default, if none is supplied, is `true`.

### Sorting

You can currently sort by the columns `created_at` and `uploaded_at` by "ASC" (ascending) or "DESC" (descending) order.

### Filtering

You can currently filter by the columns `created_at` and `uploaded_at`.\
You may choose a DATE value on which to filter: "`filter_from`" (all the entries from a value), "`filter_to`" (all the values to a value) or "`filter_from`" and "`filter_to`" (all the entries between two values).
# Get Project

Export the project definition, mapping and stats for a particular Project. If the project is private, an `access_token` must be provided (See: API Authentication).

We assume the base domain to be **five.epicollect.net**.

## HTTP REQUEST

`GET /api/export/project/{project_slug}`

## Query Parameters

| Parameter     | Required            | Description                 |
| ------------- | ------------------- | --------------------------- |
| project\_slug | yes, as url segment | The slugified project name. |

## Further Descriptions

### `project_slug`

The **project\_slug** is slugified version of the project name. Any spaces in the project name are replaced by a hyphen "-" to make it url safe. To retrieve it, check the **Developers** section on your project details page. From the same page you can download the full project definition in JSON format. It is used as a segment in the request url.
# Get Media

Get the Project logo image or the media for a particular Entry Answer in a Project. If the project is private, an `access_token` must be provided. [**See API Authentication.**](../api-authentication/create-client-app)

We assume the base domain to be **five.epicollect.net**.

## HTTP REQUEST

`GET /api/export/media/{project_slug}?{key=value&key=value...}`

## Query Parameters

| Parameter     | Required            | Description                 |
| ------------- | ------------------- | --------------------------- |
| project\_slug | yes, as url segment | The slugified project name. |
| type          | yes                 | The type of media.          |
| format        | yes                 | The format of the media.    |
| name          | yes                 | The name of the media.      |

## Further Descriptions

### `project_slug`

The **project\_slug** is slugified version of the project name. Any spaces in the project name are replaced by a hyphen "-" to make it url safe. To retrieve it, check the **Developers** section on your project details page. From the same page you can download the full project definition in JSON format. It is used as a segment in the request url.

### `type`

The **type** must be one of the following: `photo`, `audio` or `video`.

### `format`

The **format** must be one of following, depending on the **type**:

| Format                | Type  | Description                       | Resolution |
| --------------------- | ----- | --------------------------------- | ---------- |
| project\_thumb        | photo | The Project logo thumbnail image. | 512x512px  |
| project\_mobile\_logo | photo | The Project logo mobile image.    | 128x128px  |
| entry\_original       | photo | The entry original photo image.   | 1024x768px |
| entry\_thumb          | photo | The entry photo thumbnail image.  | 100x100px  |
| audio                 | audio | The entry original audio.         | n/a        |
| video                 | video | The entry original video.         | n/a        |

### `name`

The **name** is the name of the media file.\
For the project logo, this will be `logo.jpg`.\
For entry media, this will be the entry answer.\
\
[**See code examples**](../examples/getting-media)
# Project Search

Search for a Project. The response given is an array objects, each of which represents a project whose name **contains** the `project_name` string. Each object includes the project `name`, `slug`, `access` and `ref`.

We assume the base domain to be **five.epicollect.net**.

## HTTP REQUEST

`GET /api/projects/{project_name}`

## Query Parameters

| Parameter     | Required            | Description                     |
| ------------- | ------------------- | ------------------------------- |
| project\_name | yes, as url segment | A full or partial project name. |

## Further Descriptions

### `project_name`

The **project\_name** parameter can be the full or partial name of a project you wish to search for. This must be **at least 3 characters long**.
# Create Client App

In order to access a private project's resources via the API, you can **create a project App**. This is suitable for machine-to-machine authentication, for example in a scheduled job which is performing tasks over the API.

In order to create a project App, you must login to Epicollect5 and either create a new project or access the details page for an existing project. From here, select the 'Apps' menu option on the left hand side and click 'Create New App'. Enter your 'App Name' and click 'Create'.

You will need to make a note of your **Client ID** and **Client Secret**, which are used when requesting access tokens.

PLEASE NOTE: currently only one project App may be created per project and anyone who has access to the project details page may add or remove a project App (the project Creator and project Managers).

## Revoke Token

If, for whatever reason, you need to revoke a live `access_token` (for example if you suspect the token has been compromised), you can revoke a token via the 'Revoke Token' button on the project App from the 'Apps' page on the project details page.

## Delete App

You can delete a project App at any time, via the 'Delete' button on the project App from the 'Apps' page on the project details page.

## Further Information

The Epicollect5 Client Credentials Grant flow is based on Laravel Passport's implementation:

[https://laravel.com/docs/5.4/passport](https://laravel.com/docs/5.4/passport)
# Retrieve Token

Once you have set up a project App, you can then request an access token using your **Client ID** and **Client Secret**.

{% hint style="warning" %}
Access tokens are valid for **2 hours** from the time they are issued.

To help prevent abuse and ensure fair use for all users, we currently enforce a **rate limit of 10 tokens per hour per IP address**.\
This restriction helps protect the system from automated misuse and excessive traffic from a single source.
{% endhint %}

## HTTP REQUEST

We assume the base domain is **five.epicollect.net**

`POST /api/oauth/token`

therefore `https://five.epicollect.net/api/oauth/token`

## POST Parameters

| Parameter      | Required | Description                            |
| -------------- | -------- | -------------------------------------- |
| grant\_type    | yes      | Must have value 'client\_credentials'. |
| client\_id     | yes      | The Client ID of your project App.     |
| client\_secret | yes      | The Client Secret of your project App. |

Here is an example based on our **EC5 API Private** project, using jQuery ([more on jQuery Ajax requests](http://api.jquery.com/jquery.ajax/)):

[(jsFiddle here](https://jsfiddle.net/mirko77/yy3d62n6/))

```
 var params = {
   grant_type: 'client_credentials',
   client_id: 153,
   client_secret: 'J7SZDPssR885Fo0xczGKqkJfa5XyMK8wxbrOYjio'
 }

  $.ajax({
   url: 'https://five.epicollect.net/api/oauth/token',
   type: 'POST',
   contentType: 'application/vnd.api+json',
   data: JSON.stringify(params),
   success: function(response) {
     console.log(JSON.stringify(response));
   },
   error: function(xhr, status, error) {
     console.log(xhr.responseText);
   }
 });
```

**Please note you cannot access the data using a browser!**

## HTTP Response

If you run the code above, this is the response you get:

```
{
  "token_type": "Bearer",
  "expires_in": 7200,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijk5OTE4YWZmMDczYjY2MjJlNWQyODVjMzJjZTM0Y2M1MTA1MDQxY2ZjOTc2MDY5ZDE4NWU5ZDQ3ZDI0MTJkYzQ4NWM0NTI2NmQyNDdhNTYzIn0.eyJhdWQiOiIyIiwianRpIjoiOTk5MThhZmYwNzNiNjYyMmU1ZDI4NWMzMmNlMzRjYzUxMDUwNDFjZmM5NzYwNjlkMTg1ZTlkNDdkMjQxMmRjNDg1YzQ1MjY2ZDI0N2E1NjMiLCJpYXQiOjE0OTQ0MjU3MzMsIm5iZiI6MTQ5NDQyNTczMywiZXhwIjoxNDk0NDMyOTMzLCJzdWIiOiIiLCJzY29wZXMiOltdfQ.S-Lsn8uP_GlUyz5fa-QUICpkyXUvFf4L4StUYYGoJCIPdqMtS7OZqbg1oJgNvCtBnqVO4LTvl7GT6-86QEIlR3d9IpHjykFYxlfOQYIlvrgx4aFwzLk5Q1cpcMFqanM-gNBhTIcq8wOSf0_2fwwKNr991hOtwFilQs4V_KwJBcQ8tpPFR0zXEnWHhmohSna9z-BCab70CTfki6UAxcT-cYG1OPrLDwodWpvRZF2UAtEn7WIRoSICnJfbtt5G21Gvn_UzwS_FxelG-on-q_l-OkgR2GiaOUuge2Ye1hDoFfBVagQhTWcQrAZOUXt9XxsBSL_YAT9uVFYJSs-x6L4kHssYtF9aR-DS8CgI6Zr9RWJMNX53r-2WAV4Idh0qXU4vdSjYFdzOa5XTsBRHHHgrU99S4LLmDySLIJDWciJ-x1owe2pTpDk_AKUA1BgtbliDPY5qGSDBQUXoA4pX-Jh9LlQVnrchTIIDmeUCKUe7ellOfE8DmvG3YcKfjB6oFIZYmdpxM6ikfBRPYTdFMzSGtsM5YHjWaL-1CGbxcJ8Y0eaXZo1DOmlcc0SX0t66pXfyQmcchMvx_O3rze7s1kxczo2BdIOp9zd8Xf3FQT3InTGSrwE5GA3XzX04hzTMGtISvL3ZALX6g5Gl0JJ9JYCgYljPzgnrzpyAaeArShU84_I"
}
```
# Access Resources

In order to access a private project's resources over the API, you **must include a valid access token** in the `Authorization` header with each request:

`Authorization: Bearer {access_token}`

{% hint style="info" %}
Please note the entries are paginated by 50 at a time.
{% endhint %}

Examples:

* [JQuery](access-resources/jquery)
* [PHP](access-resources/php)
* [Axios](access-resources/axios)
* [Fetch](access-resources/fetch)
# JQuery

For example, using **jQuery** [**(JSFiddle)**](https://jsfiddle.net/yvbf4cw1/)

```
//Example of getting entries using jQuery

//Replace parameters with your own
var params = {
  grant_type: 'client_credentials',
  client_id: 2,
  client_secret: 'QowjYIFrWbzLEwttXzuTnb20OPbRWwlPlaNLQ6VW'
}

//perform Ajax request to get token
$.ajax({
  url: 'https://five.epicollect.net/api/oauth/token',
  type: 'POST',
  contentType: 'application/vnd.api+json',
  data: JSON.stringify(params),
  success: function(response) {
    console.log(JSON.stringify(response));
    //the token is valid for 2 hours, let's get the entries
    _getEntries(response.access_token);
  },
  error: function(xhr, status, error) {
    console.log(xhr.responseText);
  }
});

//get the entries, passing token for authorisation
//ec5-api-test is the project slug
function _getEntries(token) {
  $.ajax({
    url: 'https://five.epicollect.net/api/export/entries/ec5-api-test',
    type: 'GET',
    contentType: 'application/vnd.api+json',
    headers: {
      Authorization: 'Bearer ' + token
    },
    success: function(response) {
      //Here are the entries, just log them for now ;)
      console.log(JSON.stringify(response));

      //do what you want with the response (entries)
      // ...
    },
    error: function(xhr, status, error) {
      console.log(xhr.responseText);
    }
  });
}
```
# PHP

Using **PHP**, with [Guzzle](http://docs.guzzlephp.org/en/stable/): (Add your project credentials accordingly)

```
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Client;

 $tokenClient = new Client(); //GuzzleHttp\Client
 $tokenURL = 'https://five.epicollect.net/api/oauth/token';

 //get token first
 try {
     $tokenResponse = $tokenClient->request('POST', $tokenURL, [
         'headers' => ['Content-Type' => 'application/vnd.api+json'],
         'body' => json_encode([
             'grant_type' => 'client_credentials',
             'client_id' => {your_client_id},
             'client_secret' => '{your_client_secret}'
         ])
     ]);

     $body = $tokenResponse->getBody();
     $obj = json_decode($body);
     $token = $obj->access_token;
 } catch (RequestException $e) {
     //handle errors
     //...
 }

 //get entries now
 $entriesURL = 'https://five.epicollect.net/api/export/entries/{project_slug}';
 $entriesClient = new Client([
     'headers' => [
         'Authorization' => 'Bearer '.$token //this will last for 2 hours!
     ]
 ]);

 try {
     $response = $entriesClient-> request('GET', $entriesURL);

     $body = $response->getBody();
     $obj = json_decode($body);

     //do something with the entries
     echo '<pre>';
     print_r($obj);
     echo '</pre>';

 } catch (RequestException $e) {
     //handle errors
     //...
 }
```
# Axios

Using the Axios library ([JSFiddle](https://jsfiddle.net/mirko77/4eymak75/1/))

```

// Example of getting entries using Axios

// Replace parameters with your own credentials
const params = {
  grant_type: 'client_credentials',
  client_id: 4879,
  client_secret: 'XbIHCZHh5WQhJCaLduHSAzzddFFI6PkHA78XUZeE'
};

// Replace with your project slug
const projectSlug = "ec5-api-private";

// Perform Axios request to get token
axios.post('https://five.epicollect.net/api/oauth/token', params, {
  headers: {
    'Content-Type': 'application/vnd.api+json'
  }
})
.then(response => {
  console.log(JSON.stringify(response.data));
  // The token is valid for 2 hours, let's get the entries
  _getEntries(response.data.access_token);
})
.catch(error => {
  console.error(error.response.data);
});

// Get the entries, passing token for authorization
function _getEntries(token) {
  axios.get(`https://five.epicollect.net/api/export/entries/${projectSlug}`, {
    headers: {
      'Content-Type': 'application/vnd.api+json',
      'Authorization': `Bearer ${token}`
    }
  })
  .then(response => {
    console.log(JSON.stringify(response.data, null, 2));
    document.querySelector('.content').textContent = JSON.stringify(response.data, null, 2);
  })
  .catch(error => {
    console.error(error.response.data);
    document.querySelector('.content').textContent = JSON.stringify(error.response.data, null, 2);
  });
}

```
# Fetch API

The [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) provides a JavaScript interface for making HTTP requests and processing the responses.

Using `fetch()` [JSFiddle](https://jsfiddle.net/mirko77/28qk35mx/4)

```
// Replace parameters with your own credentials
const params = {
  grant_type: 'client_credentials',
  client_id: 4879,
  client_secret: 'XbIHCZHh5WQhJCaLduHSAzzddFFI6PkHA78XUZeE'
};

// Replace with your project slug
const projectSlug = "ec5-api-private";

// Perform Fetch request to get token
fetch('https://five.epicollect.net/api/oauth/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/vnd.api+json'
  },
  body: JSON.stringify(params)
})
.then(response => response.json())
.then(data => {
  console.log(JSON.stringify(data));
  // The token is valid for 2 hours, let's get the entries
  _getEntries(data.access_token);
})
.catch(error => {
  console.error(error);
});

// Get the entries, passing token for authorization
function _getEntries(token) {
  fetch(`https://five.epicollect.net/api/export/entries/${projectSlug}`, {
    headers: {
      'Content-Type': 'application/vnd.api+json',
      'Authorization': `Bearer ${token}`
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log(JSON.stringify(data, null, 2));
    document.querySelector('.content').textContent = JSON.stringify(data, null, 2);
  })
  .catch(error => {
    console.error(error);
    document.querySelector('.content').textContent = JSON.stringify(error, null, 2);
  });
}

```
# Getting Entries

We set up a project called [EC5 API Test](https://five.epicollect.net/project/ec5-api-test). The project is **public** so anyone can perform a GET request to fetch its entries.

Here is the response of the following GET endpoint: ([Open in browser](https://five.epicollect.net/api/export/entries/ec5-api-test))

```
https://five.epicollect.net/api/export/entries/ec5-api-test
```

```
{
  "links": {
    "self": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=&branch_owner_uuid=&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1",
    "first": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=&branch_owner_uuid=&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1",
    "prev": null,
    "next": null,
    "last": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=&branch_owner_uuid=&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1"
  },
  "meta": {
    "total": 3,
    "per_page": 50,
    "current_page": 1,
    "last_page": 1,
    "from": 1,
    "to": 1
  },
  "data": {
    "id": "ec5-api-test",
    "type": "entries",
    "entries": [
      {
        "ec5_uuid": "39f51e6d-6438-76ba-e63c-82b6b387c041",
        "created_at": "2017-04-27T14:42:04.080Z",
        "1_Name": "Megan Fox",
        "2_Age": 30,
        "3_Date_of_birth": "16/05/1986",
        "4_Sex": "Female",
        "5_Photo": "https://five.epicollect.net/api/media/ec5-api-test?type=photo&format=entry_original&name=39f51e6d-6438-76ba-e63c-82b6b387c041_1493304122.jpg"
      },
      {
        "ec5_uuid": "768bb179-fd2c-87b1-ec20-86a9acfdc87a",
        "created_at": "2017-04-27T14:38:17.564Z",
        "1_Name": "Jim Carrey",
        "2_Age": 55,
        "3_Date_of_birth": "17/01/1962",
        "4_Sex": "Male",
        "5_Photo": "https://five.epicollect.net/api/media/ec5-api-test?type=photo&format=entry_original&name=768bb179-fd2c-87b1-ec20-86a9acfdc87a_1493303895.jpg"
      },
      {
        "ec5_uuid": "e83d3770-2b55-11e7-a60a-656c7ec627a0",
        "created_at": "2017-04-27T14:29:22.663Z",
        "1_Name": "Nicholas Cage",
        "2_Age": 53,
        "3_Date_of_birth": "07/01/2017",
        "4_Sex": "Male",
        "5_Photo": "https://five.epicollect.net/api/media/ec5-api-test?type=photo&format=entry_original&name=e83d3770-2b55-11e7-a60a-656c7ec627a0_1493303578.jpg"
      }
    ],
    "mapping": {
      "map_name": "EC5_AUTO",
      "map_index": 0
    }
  }
}
```

Since we did not pass any map parameter, by default the entries are mapped against the default EC5\_AUTO mapping.

The `links` and `meta` properties contains info about how many entries there are in total and the endpoints to get the next set. By default the **entries are paginated by 50 at a time,** so you will have to write a loop to get all of them by using the `links.next` enpoint until is `null`. In the above example it is `null` already as we only have a few entries.
# Getting Branch Entries

We set up a project called [EC5 API Test](https://five.epicollect.net/project/ec5-api-test). The project is **public** so anyone can perform a GET request to fetch its entries.

Here is the response of the following GET endpoint, to retrieve all branch entries for a particular branch input: ([Open in browser](https://five.epicollect.net/api/export/entries/ec5-api-test?branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f))

```
https://five.epicollect.net/api/export/entries/ec5-api-test?branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f
```

```
{
  "links": {
    "self": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f&branch_owner_uuid=&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1",
    "first": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f&branch_owner_uuid=&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1",
    "prev": null,
    "next": null,
    "last": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f&branch_owner_uuid=&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1"
  },
  "meta": {
    "total": 4,
    "per_page": 50,
    "current_page": 1,
    "last_page": 1,
    "from": 1,
    "to": 1
  },
  "data": {
    "id": "ec5-api-test",
    "type": "entries",
    "entries": [
      {
        "ec5_branch_owner_uuid": "768bb179-fd2c-87b1-ec20-86a9acfdc87a",
        "ec5_branch_ref": "6_Family_Members",
        "created_at": "2017-05-19T12:51:41.674Z",
        "7_Name": "Andrew Carrey",
        "8_Age": 46
      },
      {
        "ec5_branch_owner_uuid": "39f51e6d-6438-76ba-e63c-82b6b387c041",
        "ec5_branch_ref": "6_Family_Members",
        "created_at": "2017-05-19T12:49:04.825Z",
        "7_Name": "Sally Fox",
        "8_Age": 28
      },
      {
        "ec5_branch_owner_uuid": "39f51e6d-6438-76ba-e63c-82b6b387c041",
        "ec5_branch_ref": "6_Family_Members",
        "created_at": "2017-05-19T12:48:57.512Z",
        "7_Name": "Bob Fox",
        "8_Age": 35
      },
      {
        "ec5_branch_owner_uuid": "39f51e6d-6438-76ba-e63c-82b6b387c041",
        "ec5_branch_ref": "6_Family_Members",
        "created_at": "2017-05-19T12:48:49.713Z",
        "7_Name": "Joe Fox",
        "8_Age": 40
      }
    ],
    "mapping": {
      "map_name": "custom",
      "map_index": 1
    }
  }
}
```

Here is the response of the following GET endpoint, to retrieve all branch entries for a particular branch input for a particular main entry: ([Open in browser](https://five.epicollect.net/api/export/entries/ec5-api-test?branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f\&branch_owner_uuid=39f51e6d-6438-76ba-e63c-82b6b387c041))

```
https://five.epicollect.net/api/export/entries/ec5-api-test?branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f&branch_owner_uuid=39f51e6d-6438-76ba-e63c-82b6b387c041
```

```
{
  "links": {
    "self": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f&branch_owner_uuid=39f51e6d-6438-76ba-e63c-82b6b387c041&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1",
    "first": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f&branch_owner_uuid=39f51e6d-6438-76ba-e63c-82b6b387c041&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1",
    "prev": null,
    "next": null,
    "last": "https://five.epicollect.net/api/export/entries/ec5-api-test?form_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273&parent_form_ref=&branch=&branch_ref=d500a44b973e4de4a80fda57ca3dfe4d_5901f6bb53273_591ee7dc8400f&branch_owner_uuid=39f51e6d-6438-76ba-e63c-82b6b387c041&parent_uuid=&uuid=&input_ref=&per_page=50&sort_order=DESC&entry_col=created_at&map_index=&page=1"
  },
  "meta": {
    "total": 3,
    "per_page": 50,
    "current_page": 1,
    "last_page": 1,
    "from": 1,
    "to": 1
  },
  "data": {
    "id": "ec5-api-test",
    "type": "entries",
    "entries": [
      {
        "ec5_branch_owner_uuid": "39f51e6d-6438-76ba-e63c-82b6b387c041",
        "ec5_branch_ref": "6_Family_Members",
        "created_at": "2017-05-19T12:49:04.825Z",
        "7_Name": "Sally Fox",
        "8_Age": 28
      },
      {
        "ec5_branch_owner_uuid": "39f51e6d-6438-76ba-e63c-82b6b387c041",
        "ec5_branch_ref": "6_Family_Members",
        "created_at": "2017-05-19T12:48:57.512Z",
        "7_Name": "Bob Fox",
        "8_Age": 35
      },
      {
        "ec5_branch_owner_uuid": "39f51e6d-6438-76ba-e63c-82b6b387c041",
        "ec5_branch_ref": "6_Family_Members",
        "created_at": "2017-05-19T12:48:49.713Z",
        "7_Name": "Joe Fox",
        "8_Age": 40
      }
    ],
    "mapping": {
      "map_name": "custom",
      "map_index": 1
    }
  }
}
```

As we did not pass any map parameter, by default the entries are mapped against the default EC5\_AUTO mapping.
# Getting Media

### Public project

We set up a project called [EC5 API Test](https://five.epicollect.net/project/ec5-api-test). The project is **public** so anyone can perform a GET request to fetch its entries. However, the same approach can be used for private projects by providing a valid \``Authorization: Bearer {value}`\` in the request, as explained in the [API authentication section](../api-authentication/access-resources)**.**

Here is the response of the following GET endpoint, to retrieve a project logo image: ([Open in browser](https://five.epicollect.net/api/export/media/ec5-api-test?type=photo\&format=project_thumb\&name=logo.jpg))

```
https://five.epicollect.net/api/export/media/ec5-api-test?type=photo&format=project_thumb&name=logo.jpg
```

Here is the response of the following GET endpoint, to retrieve an answer original image: ([Open in browser](https://five.epicollect.net/api/export/media/ec5-api-test?type=photo\&format=entry_original\&name=768bb179-fd2c-87b1-ec20-86a9acfdc87a_1493303895.jpg))

```
https://five.epicollect.net/api/export/media/ec5-api-test?type=photo&format=entry_original&name=768bb179-fd2c-87b1-ec20-86a9acfdc87a_1493303895.jpg
```

You can also get the image as a blob, useful when the project is private: ([jsFiddle](https://jsfiddle.net/mirko77/y45brprq/))

### Javascript

```
var mediaEndpoint = 'https://five.epicollect.net/api/export/media/ec5-api-test?';

 function _getEntries() {
   window.setTimeout(function() {
     $.ajax({
       url: 'https://five.epicollect.net/api/export/entries/ec5-api-test',
       type: 'GET',
       contentType: 'application/vnd.api+json',
       success: function(response) {
         var entries = response.data.entries;
         var images = [];
         var filename;

         $(response.data.entries).each(function(index, entry) {
           filename = entry.photo;

           _getMedia(mediaEndpoint + 'type=photo&format=entry_original&name=' + entry.photo)
         });
       },
       error: function(xhr, status, error) {
         console.log(xhr.responseText);
       }
     });
   }, 1000);
 }

 function _getMedia(fileUrl) {

   var myImage = document.querySelector('img');

   //uncomment and add the token to the headers if the project is private
   //var myHeaders = new Headers();
   //myHeaders.append("Authorization", 'Bearer ' + token);
   var myInit = {
     method: 'GET',
    // headers: myHeaders, //uncomment when project is private
     mode: 'cors',
     cache: 'default'
   };

   fetch(fileUrl, myInit).then(function(response) {
     return response.blob();
   }).then(function(myBlob) {
     var objectURL = URL.createObjectURL(myBlob);
     myImage.src = objectURL;
   });
 }

 _getEntries();
```

You can get the media files and download them to your server.

### PHP

Here is an example using PHP and [Guzzle](http://docs.guzzlephp.org/en/stable/index.html) (add your project credentials accordingly):

```
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Client;

$tokenClient = new Client();
$tokenURL = $this->serverURL.'/api/oauth/token';

 //get token first
 try {
     $tokenResponse = $tokenClient->request('POST', $tokenURL, [
         'headers' => [
         'Content-Type' => 'application/vnd.api+json'
         ],
         'body' => json_encode([
             'grant_type' => 'client_credentials',
             'client_id' => $this->clientId,
             'client_secret' => $this->clientSecret
         ])
     ]);

     $body = $tokenResponse->getBody();
     $obj = json_decode($body);
     $token = $obj->access_token;
 } catch (RequestException $e) {
     //handle errors
     echo $e->getMessage();
     exit();
 }

 //get media files now
 $mediaURL = $this->serverURL.'/api/export/entries/'.$this->projectSlug;

 $mediaClient = new Client([
     'headers' => [
         'Authorization' => 'Bearer '.$token //this will last for 2 hours!
     ]
 ]);

 try {
     //Get all entries for main form
     $response = $mediaClient-> request('GET', $mediaURL);
     $entries = json_decode($response->getBody())->data-> entries;

     //loop all entries to find the file names
     foreach($entries as $entry) {

        //get the media file (need to look at the project structure)
         $filename = $entry->photo;

         //build the full resolution image url
         $params='?type=photo&format=entry_original&name=';
         $photoURL = $this->serverURL.$this->mediaEndpoint.$this->projectSlug.$params.$filename;

         //get media file and save to proper location
         //IMPORTANT: you server needs to have write access to the folder you are saving the files to
         $mediaClient->request('GET', $photoURL, ['sink' => {your_server_storage_path}.'/'.$filename]);

     }
 } catch (RequestException $e) {
     //handle errors
     echo $e-> getMessage();
     exit();
 }
```

### Private project

We set up a private project for testing called [EC5 Media API Demo](https://five.epicollect.net/project/ec5-media-api-demo).

The project has a single entry with a photo.\
\
The credentials to access this project entry are as follows:

<table><thead><tr><th></th><th width="478"></th><th></th></tr></thead><tbody><tr><td>client ID</td><td>4945</td><td></td></tr><tr><td>client Secret</td><td>djCKm1JGxDJ2zwjr10I4WNkpl7QpvsAbGwimMnXr</td><td></td></tr><tr><td></td><td></td><td></td></tr></tbody></table>

Using a GET request with a proper authorization header and a valid token as explained in t[he authentication section](https://github.com/epicollect5/epicollect5-docs-developers/blob/master/examples/broken-reference/README.md) the photo will be retrieved correctly.\
\
`https://five.epicollect.net/api/export/media/ec5-media-api-demo?type=photo&name=e791b360-cf21-11ee-8f4e-0d257c6d0c4d_1708345534.jpg&format=entry_original`\\

Using [Insomnia ](https://insomnia.rest/)client:

<figure><img src="https://3821013468-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FZc6JlewNcO1tTLYsu4nH%2Fuploads%2Fgit-blob-020ef50b1044e617a251934cb965c9c7e7916d9f%2FScreenshot%202024-02-19%20at%2015.33.37.png?alt=media" alt=""><figcaption></figcaption></figure>

### JQuery

See the fiddle at [https://jsfiddle.net/mirko77/6ugLe5da/](https://jsfiddle.net/mirko77/6ugLe5da/)
# PyEpicollect

A community-built library to fetch Epicollect5 data in Python. [**View it on Github**](https://github.com/fitoprincipe/pyepicollect).

## Read EpiCollect5 data from python

* **python code**: Rodrigo E. Principe (fitoprincipe82 at gmail)
* **EpiCollect expert**: Pablo Masera (pablomasera83 at gmail)

### Install

> pip install pyepicollect

### Use

See example in binder.\
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fitoprincipe/pyepicollect/master)

### Unit Test

1.  Make a virtual environment: (see [https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv))

    > virtualenv env --python=python3

Make sure to name the environment `env` so it's ignored by git. Do not do:

> virtualenv venv --python=python3

1.  install requirments

    > pip install -r requirements.txt
2.  run test

    > python -m pytest -v
# Using R

An example of getting Epicollect5 data in R. [Get the source code here.](https://gist.github.com/mirko77/3f4a101cd4a77e2ae3e760d44d18d901)

```
library(httr)
library(jsonlite) # if needing json format

cID<-"999"      # client ID
secret<- "F00HaHa00G" # client secret
proj.slug<- "YourProjectSlug" # project slug
form.ref<- "YourFormRef" # form reference
branch.ref<- "YourFromRef+BranchExtension" # branch reference

res <- POST("https://five.epicollect.net/api/oauth/token",
            body = list(grant_type = "client_credentials",
                        client_id = cID,
                        client_secret = secret))
http_status(res)
token <- content(res)$access_token

# url.form<- paste("https://five.epicollect.net/api/export/entries/", proj.slug, "?map_index=0&form_ref=", form.ref, "&format=json", sep= "") ## if using json
url.form<- paste("https://five.epicollect.net/api/export/entries/", proj.slug, "?map_index=0&form_ref=", form.ref, "&format=csv&headers=true", sep= "")

res1<- GET(url.form, add_headers("Authorization" = paste("Bearer", token)))
http_status(res1)
# ct1<- fromJSON(rawToChar(content(res1))) ## if using json
ct1<- read.csv(res1$url)
str(ct1)

# url.branch<- paste("https://five.epicollect.net/api/export/entries/", proj.slug, "?map_index=0&branch_ref=", branch.ref, "&format=json&per_page=1000000", sep= "") ## if using json; pushing max number of records from default 50 to 10^6
url.branch<- paste("https://five.epicollect.net/api/export/entries/", proj.slug, "?map_index=0&branch_ref=", branch.ref, "&format=csv&headers=true", sep= "")

res2<- GET(url.branch, add_headers("Authorization" = paste("Bearer", token)))
http_status(res2)
ct2<- read.csv(res2$url)
# ct2<- fromJSON(rawToChar(content(res2))) ## if using json
str(ct2)
```
