# API 定义

1. resoucetype [GET] [video, image, audio, page, file,]

    描述：获取资源类型。

    参数：无。

    返回值：视频、图片、音频、页面或文件的类型。

2. resourceid [GET] [video id, image id, audio id, page id, file id, live id,]

    描述：获取资源的唯一标识符。

    参数：无。

    返回值：视频、图片、音频、页面或文件的唯一标识符。

3. createtime [GET] [date, time,]

    描述：获取资源的创建时间。

    参数：无。

    返回值：资源的创建时间，包括日期和时间。

4. action [GET] [play, pause, stop, download, upload,]

    描述：对资源执行的操作。

    参数：无。

    返回值：执行的操作结果。

5. params [GET] [video: {start, end}, image: {width, height}, audio: {start, end}, page: {page, size}, file: {size},]

    描述：资源的参数设置。

    参数：无。

    返回值：视频、图片、音频、页面或文件的参数设置。
