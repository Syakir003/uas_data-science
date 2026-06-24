# app.py
from flask import Flask, render_template, request

import data_loader
import clustering

app = Flask(__name__)


@app.route('/')
def index():
    error = None
    preview = None
    try:
        data = data_loader.load_data()
        preview = data.head().to_html(
            classes='table table-sm table-striped mb-0', index=False, na_rep='-')
    except FileNotFoundError as exc:
        error = str(exc)
    return render_template('index.html', preview=preview, error=error)


@app.route('/result', methods=['POST'])
def result():
    k = int(request.form.get('k', 3))
    feature_group = request.form.get('features', 'keduanya')

    data = data_loader.load_data()
    total_prov = len(data)
    clean, features = clustering.prepare_features(data, feature_group)
    dropped = total_prov - len(clean)

    # validasi: k tidak boleh melebihi jumlah provinsi
    if k > len(clean):
        k = len(clean)

    result_df, silhouette = clustering.run_clustering(clean, features, k)
    ks, inertias, _ = clustering.compute_elbow(clean, features)

    has_miskin = feature_group in ('kemiskinan', 'keduanya')
    has_ipm = feature_group in ('ipm', 'keduanya')

    return render_template(
        'result.html',
        k=k,
        feature_group=feature_group,
        n_prov=len(clean),
        dropped=dropped,
        silhouette=round(silhouette, 3),
        elbow_html=clustering.make_elbow_chart(ks, inertias),
        scatter_html=clustering.make_scatter_chart(result_df, feature_group),
        box_miskin_html=clustering.make_boxplot(result_df, 'Miskin_2025',
                                                'Kemiskinan 2025 per Cluster') if has_miskin else None,
        box_ipm_html=clustering.make_boxplot(result_df, 'IPM_2025',
                                             'IPM 2025 per Cluster') if has_ipm else None,
        profile=clustering.cluster_profile(result_df, features),
        provinces=clustering.provinces_by_cluster(result_df),
        cluster_colors=clustering.CLUSTER_COLORS,
    )


if __name__ == '__main__':
    app.run(debug=True)
