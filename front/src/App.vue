<template>
    <div id="app">
        <el-container>
            <el-header>
                <el-card :body-style="{ padding: '0px' }">
                    <el-input  ref="inputRef" v-model="rawUrl" @keyup.enter.native="doshortUrl" @blur="doshortUrl" placeholder="输入链接并按下 Enter 回车键"></el-input>
                </el-card>
            </el-header>
            <el-main>
                <el-row :gutter="20">
                    <el-col :span="10" :xs="24" :lg="6">
                        <div class="grid-content">
                            <el-card :body-style="{height: '235px' }">
                                <!-- <img src="" class="image"> -->
                                <div id="qrcode" ref="qrCodeUrl">
                                    <div id="qrcodeImg"></div>
                                </div>
                            </el-card>
                        </div>
                    </el-col>
                    <el-col :span="14" :xs="24" :lg="18">
                        <div class="grid-content">
                            <el-card :body-style="{ padding: '5px', margin: '5px' }">
                                <el-link :underline="false">
                                    {{ shortUrl }}
                                </el-link>&nbsp;&nbsp;
                                <el-button v-if="shortUrl" type="text" class="button" v-clipboard:copy="shortUrl" v-clipboard:success="onCopy">复制</el-button>
                            </el-card>
                        </div>
                    </el-col>
                </el-row>
            </el-main>
        </el-container>
    </div>
</template>
<script>
import QRCode from 'qrcodejs2'

console.log(process.env)

export default {
    name: 'App',
    mounted() {
        this.$refs.inputRef.$el.children[0].focus();
    },
    methods: {
        doshortUrl() {
            console.log(this.$http.defaults)
            var baseURL = this.$http.defaults.baseAPIURL;
            if (this.rawUrl != '') {
                this.$http.post(baseURL + '/g/', {
                    url: this.rawUrl
                }).then(resp => {
                    this.shortUrl = baseURL + '/a/' + resp.data.code;
                    this.createQrcode(this.shortUrl);
                })
            }
        },
        createQrcode(text) {
            const qrcodeImgEl = document.getElementById('qrcodeImg')
            qrcodeImgEl.innerHTML = ''
            let qrcode = new QRCode(qrcodeImgEl, {
                width: 235,
                height: 235,
                colorDark: '#000000',
                colorLight: '#ffffff'
            })
            qrcode.makeCode(text)
        },
        onCopy() {
            this.$message({
                message: 'copied',
                type: 'success'
            });
        },
    },
    data() {
        return {
            rawUrl: '',
            shortUrl: ''
        }
    }
}
</script>
<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}


.el-col {
    margin-bottom: 20px;

    &:last-child {
        margin-bottom: 0;
    }
}

.bg-purple-dark {
    background: #99a9bf;
}

.bg-purple {
    background: #d3dce6;
}

.bg-purple-light {
    background: #e5e9f2;
}
</style>