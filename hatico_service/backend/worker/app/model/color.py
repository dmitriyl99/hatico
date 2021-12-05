from sklearn.cluster import KMeans
from collections import Counter


class ColorDetectionModel:
    COLORS_DARK: int = 1
    COLORS_LIGHT: int = 2
    COLORS_MULTICOLOR = 3

    def _detect_color(self, image):
        # получим высоту и ширину изображения
        (h, w) = image.shape[:2]
        # вырежем участок изображения используя срезы
        cropped = image[int(h / 4): int(h * 3 / 4), int(w / 4): int(w * 3 / 4)]
        # кластеризуем пиксели изображения
        number_of_colors = 2
        modified_image = cropped.reshape(cropped.shape[0] * cropped.shape[1], 3)
        clf = KMeans(n_clusters=number_of_colors, random_state=7)
        labels = clf.fit_predict(modified_image)
        counts = Counter(labels)
        center_colors = clf.cluster_centers_
        ordered_colors = [center_colors[i] for i in counts.keys()]
        rgb_colors = [ordered_colors[i] for i in counts.keys()]
        # 0.5 норма, заменила на 0.7
        color = (
            "light"
            if (
                    1
                    - (
                            0.299 * rgb_colors[0][0]
                            + 0.587 * rgb_colors[0][1]
                            + 0.114 * rgb_colors[0][2]
                    )
                    / 255
                    < 0.73
            )
            else "dark"
        )
        return color

    def _most_frequent_color(self, colors):
        light_count = colors.count('light')
        dark_count = colors.count('dark')
        if light_count == dark_count:
            return self.COLORS_MULTICOLOR
        if light_count > dark_count:
            return self.COLORS_LIGHT
        if light_count < dark_count:
            return self.COLORS_DARK

    def predict(self, images: list):
        colors = []
        for image in images:
            colors.append(self._detect_color(image))
        return self._most_frequent_color(colors)
