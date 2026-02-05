## Setup

pip install -r requirements.txt

pip install instagrapi==2.2.1

pip install -e .


# PATCHED: instagrapi broadcast extractor assumes pinned_channels_info exists

in package file at--> virtual-env/lib/python3.12/site-packages/instagrapi/extractors.py

where:

```python
def extract_broadcast_channel(data):
    """ Extract broadcast channel infos """
    channels = data["pinned_channels_info"]["pinned_channels_list"]
    return [Broadcast(**channel) for channel in channels]

```

replace with:

```python
def extract_broadcast_channel(data):
    """ Extract broadcast channel infos """
    #channels = data["pinned_channels_info"]["pinned_channels_list"]
    pci = data.get("pinned_channels_info") or {}
    channels = pci.get("pinned_channels_list") or []
    return [Broadcast(**channel) for channel in channels]
```


