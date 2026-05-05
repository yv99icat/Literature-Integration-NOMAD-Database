# ------------------------------ 
# PREPARE DATA FOR MANUAL NOMIC UPLOAD
# ------------------------------ 

import pandas as pd
import numpy as np
import os

# Create output directory
os.makedirs('./nomic_upload', exist_ok=True)

print("Preparing data for manual Nomic Atlas upload...")

# Option 1: CSV with embeddings and metadata (RECOMMENDED)
# This gives you the most control and works reliably
upload_data = []

for i, (text, cluster_id, embedding) in enumerate(zip(texts, cluster_labels, stella_embeddings)):
    # Get cluster topic keywords
    cluster_topic = ', '.join(topics.get(cluster_id, ['Unknown'])[:5]) if cluster_id != -1 else 'Noise'
    
    # Create comprehensive metadata
    row = {
        'id': str(i),
        'text': text[:2000] + ('...' if len(text) > 2000 else ''),  # Keep substantial text
        'full_abstract': text,  # Keep full text too
        'cluster_id': cluster_id,
        'cluster_topic': cluster_topic,
        'is_noise': cluster_id == -1,
        'abstract_length': len(text),
        'word_count': len(text.split()),
    }
    
    # Add embedding dimensions as separate columns
    for dim in range(stella_embeddings.shape[1]):
        row[f'embedding_{dim}'] = embedding[dim]
    
    upload_data.append(row)

# Create the upload DataFrame
upload_df = pd.DataFrame(upload_data)

# Save main upload file
upload_df.to_csv('./nomic_upload/perovskite_research_with_embeddings.csv', index=False)
print("✅ Main upload file saved: ./nomic_upload/perovskite_research_with_embeddings.csv")

# Option 2: Separate files approach
# Sometimes easier to manage large datasets

# Save embeddings separately (NPY format that Nomic can read)
np.save('./nomic_upload/stella_embeddings.npy', stella_embeddings)
print("✅ Embeddings saved: ./nomic_upload/stella_embeddings.npy")

# Save metadata only CSV
metadata_df = upload_df.drop([col for col in upload_df.columns if col.startswith('embedding_')], axis=1)
metadata_df.to_csv('./nomic_upload/metadata_only.csv', index=False)
print("✅ Metadata file saved: ./nomic_upload/metadata_only.csv")

# Save cluster summary for reference
cluster_summary = pd.DataFrame([
    {
        'cluster_id': cluster_id, 
        'keywords': ', '.join(keywords),
        'document_count': sum(cluster_labels == cluster_id),
        'percentage': f"{(sum(cluster_labels == cluster_id) / len(cluster_labels) * 100):.1f}%"
    }
    for cluster_id, keywords in topics.items()
])
cluster_summary = cluster_summary.sort_values('document_count', ascending=False)
cluster_summary.to_csv('./nomic_upload/cluster_summary.csv', index=False)
print("✅ Cluster summary saved: ./nomic_upload/cluster_summary.csv")

# Create a simple 2D UMAP for backup visualization
try:
    import umap
    print("Creating 2D projection for backup...")
    
    umap_2d = umap.UMAP(n_components=2, random_state=42)
    embeddings_2d = umap_2d.fit_transform(stella_embeddings)
    
    # Add 2D coordinates to metadata
    metadata_with_2d = metadata_df.copy()
    metadata_with_2d['umap_x'] = embeddings_2d[:, 0]
    metadata_with_2d['umap_y'] = embeddings_2d[:, 1]
    metadata_with_2d.to_csv('./nomic_upload/metadata_with_2d_umap.csv', index=False)
    print("✅ 2D UMAP projection saved: ./nomic_upload/metadata_with_2d_umap.csv")
    
except Exception as e:
    print(f"⚠️  Could not create 2D projection: {e}")

print(f"""
🎉 Files prepared for manual Nomic Atlas upload!

📁 Files created in ./nomic_upload/:
   1. perovskite_research_with_embeddings.csv  ← Main file (embeddings + metadata)
   2. stella_embeddings.npy                    ← Just embeddings
   3. metadata_only.csv                        ← Just metadata
   4. cluster_summary.csv                      ← Cluster analysis summary
   5. metadata_with_2d_umap.csv               ← Metadata + 2D coordinates

📊 Dataset Stats:
   • Total documents: {len(texts)}
   • Embedding dimensions: {stella_embeddings.shape[1]}
   • Number of clusters: {len(topics)}
   • Noise points: {sum(cluster_labels == -1)}

🚀 Upload Instructions:
   1. Go to https://atlas.nomic.ai
   2. Click "Create New Map"
   3. Upload 'perovskite_research_with_embeddings.csv'
   4. Nomic will auto-detect embeddings and metadata
   5. Set 'text' as your text field
   6. Set 'cluster_id' and 'cluster_topic' as colorable fields
""")

# Print file sizes for reference
for filename in ['perovskite_research_with_embeddings.csv', 'stella_embeddings.npy', 'metadata_only.csv']:
    filepath = f'./nomic_upload/{filename}'
    if os.path.exists(filepath):
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"   📄 {filename}: {size_mb:.1f} MB")