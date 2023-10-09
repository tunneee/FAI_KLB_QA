from utils.utils import *
import streamlit as st

st.title("Video Text Retrieval")

st.sidebar.title("Utils")
st.sidebar.subheader("Video")
# video_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", "avi", "asf", "m4v"])
# if video_file is not None:
#     upload_new_videos_to_db(video_file)

upload_button = st.sidebar.button("Upload all videos in samples into Database")
if upload_button:
    for file in os.listdir(dataset_path):
        upload_new_videos_to_db(dataset_path, file)
create_collection_button = st.sidebar.button("Create collection")
if create_collection_button:
    create_collection(collection_name)

delete_collection_button = st.sidebar.button("Delete collection")
if delete_collection_button:
    delete_collection(collection_name)


user_input = st.text_area("Enter your text here", height=300)

if st.button("Submit"):
    results = search_with_query(user_input)
    if len(results) == 0:
        st.write("No results found")
    for res in results:
        # st.write(res)
        
        res = dict(res)
        # st.write(res)
        img_url = res["payload"]['url'] 
        video_url = res["payload"]['video_url']
        frame_rate = res["payload"]['fps']
        frame_idx = img_url.split("/")[-1].split(".")[0].split("_")[-1]
        start_time = int(frame_idx) / frame_rate
        raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB') 
        st.write(f"Found video at {video_url} with start time {round(start_time, 2)} seconds with score {round(res['score'], 2)}")
        st.image(raw_image, width=200)
        st.video(video_url, start_time=int(start_time))
        st.divider()



