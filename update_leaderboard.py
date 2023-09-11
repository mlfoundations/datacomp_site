import pandas as pd

import firebase_admin
from firebase_admin import credentials, db

# Read baselines data
baselines_fname = '/admin/home-gamaga/datacomp_site/data/baselines.csv'
data = pd.read_csv(baselines_fname)

# Add common info
data['author'] = 'DataComp team'
data['writeup'] = 'https://arxiv.org/abs/2304.14108'


# Read external data from firebase
cred = credentials.Certificate('/admin/home-gamaga/firebase_key.json')
config = {'databaseURL': 'https://laion-tng-default-rtdb.firebaseio.com/'}
firebase_admin.initialize_app(cred, config)

ref = db.reference('/')
fb_data = ref.get()


# Add data from firebase
datasets = ['CIFAR-10', 'CIFAR-100', 'CLEVR Counts', 'CLEVR Distance', 'Caltech-101', 'Camelyon17', 'Country211', 'Describable Textures', 'Dollar Street', 'EuroSAT', 'FGVC Aircraft', 'FMoW', 'Flickr', 'Food-101', 'GTSRB', 'GeoDE', 'ImageNet 1k', 'ImageNet Sketch', 'ImageNet v2', 'ImageNet-A', 'ImageNet-O', 'ImageNet-R', 'KITTI Vehicle Distance', 'MNIST', 'MSCOCO', 'ObjectNet', 'Oxford Flowers-102', 'Oxford-IIIT Pet', 'Pascal VOC 2007', 'PatchCamelyon', 'RESISC45', 'Rendered SST2', 'STL-10', 'SUN397', 'SVHN', 'Stanford Cars', 'WinoGAViL', 'iWildCam']

for key, info in fb_data.items():
    imagenet_acc = info['ImageNet 1k']
    accs = [info[dataset] for dataset in datasets]
    avg_acc = sum(accs) / len(accs)

    date = info['timestamp'].split('_')[0]
    sd = date.split('-')
    date = '-'.join([sd[1], sd[2], sd[0]])

    writeup = info.get('writeup', '')

    try:
        row = {
            'track': info['track'],
            'scale': info['scale'],
            'date': date,
            'name': info['method_name'],
            'imagenet_acc': f'{imagenet_acc:.3f}',
            'avg_acc': f'{avg_acc:.3f}',
            'dataset_size': info['dataset_size'],
            'author': info['author'],
            'writeup': writeup
        }
    except KeyError as e:
        print(f'Key error for {key}.\nFull info: {info}')
        print(e)
        import sys; sys.exit()

    data = data.append(row, ignore_index=True)

# Write csvs
tracks = ['filtering', 'byod']
scales = ['small', 'medium', 'large', 'xlarge']

for scale in scales:
    for track in tracks:
        df = data[(data['track'] == track) & (data['scale'] == scale)]
        df = df.drop(['track', 'scale'], axis=1)
        track = track.replace('ing', '')
        df.to_csv(f'data/{track}_{scale}.tsv', header=False, index=False, sep='\t')

