const recorderManager = wx.getRecorderManager()
const innerAudioContext = wx.createInnerAudioContext()
var init

Page({

        /**
         * 页面的初始数据
         */
        data: {
            time: 0, //录音时长
            duration: 30000, //录音最大值ms 30000/30秒
            tempFilePath: "", //音频路径
            status: 0, //录音状态 0:未开始录音 1:正在录音 2:暂停录音 3:已完成录音
            playStatus: 0, //录音播放状态 0:未播放 1:正在播放
            uploaded: 0, //录音是否已上穿，0:未上传 1:已上传
            backcolor: 'green', //按钮背景颜色
            voiceres: '语音分析中...',
            btn_start: false,
            btn_rec: true,
            btn_rtn: true,
        },

        /**
         * 生命周期函数--监听页面加载
         */
        onLoad: function (options) {

        },

        /**
         * 生命周期函数--监听页面初次渲染完成
         */
        onReady: function () {

        },

        /**
         * 生命周期函数--监听页面显示
         */
        onShow: function () {

        },

        /**
         * 生命周期函数--监听页面隐藏
         */
        onHide: function () {

        },

        /**
         * 生命周期函数--监听页面卸载
         */
        onUnload: function () {

        },

        /**
         * 页面相关事件处理函数--监听用户下拉动作
         */
        onPullDownRefresh: function () {

        },

        /**
         * 页面上拉触底事件的处理函数
         */
        onReachBottom: function () {

        },

        /**
         * 用户点击右上角分享
         */
        onShareAppMessage: function () {

        },

        /**开始录音 */
        handleRecordStart: function () {
            clearInterval(init) //清除定时器
            // 监听音频开始事件
            recorderManager.onStart((res) => {
                console.log('recorder start')
                this.setData({
                    status: 1,
                    uploaded: 0,
                    backcolor: 'red',
                })
            })

            //监听录音自动结束事件(如果不加，录音时间到最大值自动结束后，没获取到录音路径将无法正常进行播放)
            recorderManager.onStop((res) => {
                console.log('recorder stop', res)
                this.setData({
                    tempFilePath: res.tempFilePath,
                    status: 3,
                    backcolor: 'green',
                    btn_rec: true,
                    btn_rtn: false
                })
                this.recordingTimer(this.data.time)
            })

            const options = {
                duration: this.data.duration, //指定录音的时长，单位 ms
                sampleRate: 16000, //采样率
                numberOfChannels: 1, //录音通道数
                encodeBitRate: 96000, //编码码率
                format: 'mp3', //音频格式，有效值 aac/mp3
                frameSize: 50, //指定帧大小，单位 KB
            }
            this.recordingTimer()
            recorderManager.start(options)
        },

        /**
         * 暂停录音
         */
        /**
         * 停止录音
         */
        handleRecordStop: function () {
            recorderManager.onStop((res) => {
                console.log('recorder stop', res)
                this.setData({
                    tempFilePath: res.tempFilePath,
                    status: 3,
                    backcolor: 'gray',
                    btn_rec: true,
                    btn_rtn: false,
                })
            })
            console.log('filepath', this.data.tempFilePath)
            this.recordingTimer(this.data.time)
            recorderManager.stop()
            //this.bofang()
        },
        bofang: function () {
            //音频地址
            innerAudioContext.src = this.data.tempFilePath
            //在ios下静音时播放没有声音，默认为true，改为false就好了。
            innerAudioContext.obeyMuteSwitch = false

            //点击播放
            if (this.data.playStatus == 0) {
                this.setData({
                    playStatus: 1
                })
                innerAudioContext.play()
            }
            // //播放结束
            innerAudioContext.onEnded(() => {
                innerAudioContext.stop()
                this.setData({
                    playStatus: 0
                })
            })
        },


        //录音计时器
        recordingTimer: function (time) {
            var that = this
            if (time == undefined) {
                //将计时器赋值给init
                init = setInterval(function () {
                    var time = that.data.time + 1;
                    that.setData({
                        time: time
                    })
                }, 1000);
            } else {
                clearInterval(init)
                console.log("暂停计时")
            }
        },

        /**
         * 重新录制
         */
        reset: function () {
            var that = this
            that.setData({
                time: 0, //录音时长
                tempFilePath: "", //音频路径
                status: 0,
                playStatus: 0,
                btn_rec: false,
                backcolor:'green‘',
                btn_rtn: true,

            })
            innerAudioContext.stop()
        },
        start: function () {
            var that = this
            that.setData({
                btn_start: true,
                btn_rec: false
            })
            wx.downloadFile({
                url: 'https://www.emmaliu.cn/prod-api/play/start',
                success(res) {
                    if (res.statusCode == 200) {
                        innerAudioContext.src = res.tempFilePath
                        innerAudioContext.play()
                    }
                }
            })
        },
        exit:function(){
            wx.exitMiniProgram()
        },

        upload: function () {
            var that = this
            console.log('duration', that.data.time)
            if (that.data.time < 3) {
                wx.showToast({
                    title: '录音时间太短，请重新录音',
                    icon: 'none',
                    duration: 1000
                })

            } else if (that.data.tempFilePath == '') {
                wx.showToast({
                    title: '未找到录音文件',
                    icon: 'none',
                    duration: 1000
                })
            } else {
                //进行语音发送
                wx.showLoading({
                    title: '语音上传中',
                })
                //上传录制的音频u
                wx.showToast({
                    title: 'fname',
                    icon: 'none',
                    duration: 2000
                })

                wx.uploadFile({
                    name: 'fname', //这个随便填
                    filePath: that.data.tempFilePath,
                    url: 'https://www.emmaliu.cn/prod-api/voice', //填写自己服务器的地址。
                    header: {
                        "Content-Type": "multipart/form-data" //必须是这个格式
                    },

                    success: function (event) {
                        console.log("event", event)
                        var datas = JSON.parse(event.data);
                        if (datas.status == 1) {
                            
                            var rtn = datas.voiceUrl

                            if (datas.result) {
                                that.setData({
                                    voiceres: datas.result,
                                    uploaded: 1,
                                    btn_rec: false,
                                    btn_rtn: true,
                                })
                                wx.showToast({
                                    title: '上传音频成功,' + rtn,
                                    icon: 'none',
                                    duration: 2000
                                })

                                wx.downloadFile({
                                    url: 'https://www.emmaliu.cn/prod-api/play/' + rtn,
                                    success(res) {
                                        console.log(res.tempFilePath)
                                        if (res.statusCode == 200) {
                                            innerAudioContext.src = res.tempFilePath
                                            innerAudioContext.play()
                                        }
                                    }
                                })

                            } else {
                                wx.showToast({
                                    title: '上传文件失败',
                                    icon: 'none',
                                    duration: 2000
                                })
                            }
                        } else {
                            wx.showToast({
                                title: "failed",
                                icon: 'none',
                                duration: 2000
                            })
                        }
                        
            that.reset()
                    },
                    fail(err) {
                        console.log("error", err)
                        wx.showToast({
                            title: err,
                            icon: 'none',
                            duration: 2000
                        })
                    }
                })
            }
            wx.hideLoading()
        }

    },
)