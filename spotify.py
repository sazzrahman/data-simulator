import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


import boto3
import json
import os



s3 = boto3.client('s3')

S3_BUCKET = os.getenv("BUCKET")

SPOTIPY_CLIENT_ID= os.getenv("CLIENT")
SPOTIPY_CLIENT_SECRET= os.getenv("SECRET")


spotify = spotipy.Spotify(client_credentials_manager=\
    SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET),requests_timeout=10)



def get_key_items(key):
    return json.loads(s3.get_object(Bucket=S3_BUCKET,Key=f"spotify/trackidx/{key}.json")["Body"].read())


def get_track_ids(pl):
    track_ids = []
    for t in pl["items"]:
        track_ids.append(t["track"]["id"])
    return track_ids



def get_spotify_tracks(idx):
    s3_client=s3
    bucket_name=S3_BUCKET
    counter = 0

    obj = get_key_items(idx)
    
    for item in obj:

        for schedule_id, pl_url in item.items():
        
            try:
                
                current_tracks = spotify.playlist_tracks(playlist_id=pl_url)
                current_tracks["clubready_id"] = schedule_id
                
                track_ids = get_track_ids(current_tracks)
                
                current_features = spotify.audio_features(track_ids)

                counter+=1

                s3_client.put_object(Body=json.dumps(current_tracks), Bucket=bucket_name, Key=f"spotify/playlists/{schedule_id}.json")
                s3_client.put_object(Body=json.dumps(current_features), Bucket=bucket_name, Key=f"spotify/audiofeatures/{schedule_id}.json")
            except spotipy.SpotifyException:
                pass
            except AttributeError:
                pass
    return "All Tracks Downloaded. Yay"