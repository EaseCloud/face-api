Face Recognition Web Service
============================

### Web API Usage

#### 1. Upload a image with single face of <face_id> to the group <group_id>.

##### Request

```
Path: /upload/<group_id>/<face_id>
Method: POST
Content-Type: multipart/form-data
Payload:
  file=<Image File Object>
```

##### Response (Success)

```
Status: 200
Content-Type: application/json
Payload:
  {"ok":true,"msg":"Upload success: group_id=<group_id> face_id=<face_id>"}
```

#### 2. Recognize the matching faces upload in the group <group_id>.

##### Request

```
Path: /recognize/<group_id>
Method: POST
Content-Type: multipart/form-data
Payload:
  file=<Image File Object>
  keys=Alice|Bob|Cathy  (Optional)
```

##### Response (Success)

```
Status: 200
Content-Type: application/json
Payload:
  {"ok":true,"msg":"Matched <n> faces.","data":["<face_id_1>","<face_id_2>",...]}
```

#### 3. Fail cases: Any expected failure will cause a 400 response with reason message.

##### Response (Success):

```
Status: 400
Content-Type: application/json
Payload:
{"ok":false,"msg":"<reason>"}
```

### CLI Usage:

See `./main.py --help` form more information.

#### 1. Run the server

```
./main.py runserver
```

Or ignore the default command name:

```
./main.py
```

#### 2. Upload a image with single face of <face_id> to the group <group_id>.

```
./main.py upload <group_id> <face_id> --file <image_path>
```

#### 3. Recognize the matching faces upload in the group <group_id>.

Matches all the faces in the group.

```
./main.py recognize <group_id> --file <image_path>
```

Matches the faces with specific face names in the group.

```
./main.py recognize <group_id> [<face1>|<face2>|...] --file <image_path>
```
