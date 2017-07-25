<template>
  <div>
  <p class="header"></p>
  <el-input
      type="textarea"
      :autosize="{ minRows: 5, maxRows: 10}"
      placeholder="请输入内容"
      v-model="content" contenteditable="true">
  </el-input>
  <div class="icon clearfix">
      <i class="icon iconfont icon-face" @click="showEmoji = !showEmoji"></i>
      <transition name="fade" mode="">
        <div class="emoji-box" v-if="showEmoji" >
          <el-button
            class="pop-close"
            :plain="true"
            type="danger"
            size="mini"
            icon="close"
            @click="showEmoji = false"></el-button>
            <vue-emoji
              @select="selectEmoji">
            </vue-emoji>
          <span class="pop-arrow arrow"></span>
        </div>
      </transition>
    </div>
    <div class="upload">
      <el-upload :on-remove="handleRemove" :file-list="fileList"
                 :action='API_URL + "/upload"' :on-change="handleChange">
        <a class="document"><i class="el-icon-document"></i></a>
      </el-upload>
    </div>
    <el-dialog title="发送消息" :visible.sync="dialogVisible">
      <h4>你输入的内容是：</h4>
      <p v-html="emoji(content)" class="content"></p>
      <ul class="el-upload-list el-upload-list--picture" v-if="fileList">
        <li class="el-upload-list__item is-success" v-for="file in fileList">
          <img :src="[API_URL + '/uploads/' + file.name]" class="el-upload-list__item-thumbnail">
          <a class="el-upload-list__item-name">
            <i class="el-icon-document"></i>{{ file.name }}
          </a>
          <label class="el-upload-list__item-status-label">
            <i class="el-icon-upload-success el-icon-check"></i>
          </label>
          <i class="el-icon-close"></i>
        </li>
    </ul>
      <div class="switch" v-if="queryType !== 'contact'">
        <el-switch v-model="sendType" on-text="发给群聊" off-text="发给用户" on-color="#13ce66" off-color="#ff4949" width=100>
        </el-switch>
      </div>

      <el-autocomplete v-if="!sendType && queryType !== 'contact'" v-model="group" placeholder="请输入群聊名字" :fetch-suggestions="querySearch" size="large" custom-item="msg-item" @select="handleSelectGroup">
      </el-autocomplete>

      <div v-if="!sendType">
        <h4>选择要发送的好友：</h4>
        <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入好友昵称" v-model="ids" :data="allMembers" :titles="['好友列表', '已选好友']">
        </el-transfer>
      </div>
      <div v-else>
        <h4>选择要发送的群聊：</h4>
        <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入群聊昵称" v-model="ids" :data="allGroups" :titles="['群聊列表', '已选群聊']">
        </el-transfer>
      </div> 
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submit">确 定</el-button>
      </div>
    </el-dialog>
    <el-button type="success" @click="dialogVisible = true" class="submit">提交</el-button>
    </div>
  </div>

</template>

<script>
  import Vue from 'vue'
  import '../../plugins/emoji/src/assets/css/iconfont.css'
  import vueEmoji from '../../plugins/emoji/src/components/emoji.vue'
  import { getUserList, getAllGroups, sendMessage, API_URL } from '../../api/api';

  Vue.component('msg-item', {
    functional: true,
    render: function (h, ctx) {
      var item = ctx.props.item;
      return h('li', ctx.data, [
        h('img', { attrs: { style: 'float: left; width: 38px; padding: 2px; margin-right: 5px',
                            src: item.avatar } }),
        h('span', { attrs: { style: '' } }, [item.label])
      ]);
    },
    props: {
      item: { type: Object, required: true }
    }
  });

	export default {
		data() {
      return {
        API_URL: API_URL,
        content: '',
        showEmoji: false,
        dialogVisible: false,
        ids: [],
        fileList: [],
        sendType: false,
        gid: '',
        emojiList: [],
        curOptions: [],
        group: '',
        groups: [],
        allMembers: [],
        allGroups: [],
        filterMethod(query, item) {
           return item.label.indexOf(query) > -1;
        },
      }
		},
    props: ['queryType'],
		methods: {
      getMembers () {
         const users = [];
         let para = {
           gid: this.gid,
           page: 0,
           q: '',
           type: this.queryType
         };
         getUserList(para).then((res) => {
            res.data.users.forEach((member, index) => {
              users.push({
                label: member.nick_name,
                key: member.id
              });
            });
            this.allMembers = users;
          });
      },
      selectEmoji (code) {
        this.emojiList.push(code);
        this.showEmoji = false
        this.content += code
      },
      handleSelectGroup(item) {
        this.gid = item.key;
        this.getMembers();
      },
      handleChange(_, fileList) {
        this.fileList = fileList;
      },
      handleRemove(_, fileList) {
        this.fileList = fileList;
      },
      submit () {
        let content = this.content
        this.emojiList.forEach((code, index) => {
          content = content.replace(code, `[${ code.slice(1, -1).replace(/\b\w/g, l => l.toUpperCase()) }]`);
        });
        let para = {
          type: this.queryType,
          gid: this.gid || '',
          content: this.content,
          ids: this.ids,
          send_type: this.sendType ? 'group': 'contact',
          files: this.fileList.map(item => item.name)
        }
        sendMessage(para).then((res) => {
          this.$checkStatus(res);
          this.content = ''
          this.fileList = []
        });
        this.dialogVisible = false
      },
      querySearch(query, cb) {
        let groups = this.allGroups;
        var results = query ? groups.filter(this.createFilter(query)) : groups;
        cb(results);
      },
      createFilter(query) {
        return (item) => {
          return item.label.toLowerCase()
                .indexOf(query.toLowerCase()) > -1;
        }
      }
		},
    components: {
      vueEmoji
    },
    mounted() {
      let getMembers = true;
      let type = this.queryType;
      let ids = this.$route.query['ids'] || '';
      if ('type' in this.$route.query) {
        type = this.$route.query['type']
      }
      if ('send_type' in this.$route.query) {
          this.sendType = true
      }
      if (ids) {
        this.ids = ids.split(',');
      }

      if (type === 'group') {
        let gid = this.$route.query['gid'] || '';
        getAllGroups().then((res) => {
          let groups = [];
          res.data.groups.forEach((member, index) => {
               groups.push({
                 label: member.nick_name,
                 key: member.id,
                 value: member.nick_name,
                 avatar: member.avatar
               });
             });
             this.allGroups = groups;
        });
        if (gid) {
          this.gid = gid;
          getMembers = true;
        } else {
          getMembers = false; 
        }
      }
      if (getMembers) {
        this.getMembers();
      }
	}
}
</script>

<style lang="scss" scoped>
ul{
  margin: 0;
  padding: 0;
  list-style: none;
}

.highlighted {
  color: #ddd;
}

.el-dialog__title {
  font-size: 18px;
}
.icon {
  position: relative;
  margin-top: 20px;
  display: inline-block;
  .iconfont {
    cursor: pointer;
    color: #F7BA2A;
  }
  .emoji-box {
    position: absolute;
    z-index: 10;
    left: -10px;
    top: 24px;
    box-shadow: 0 4px 20px 1px rgba(0, 0, 0, 0.2);
    background: white;
    .el-button {
      position: absolute;
      border: none;
      color: #FF4949;
      right: 12px;
      top: 12px;
      z-index: 10;
    }
    .arrow {
      left: 10px;
    }
  }
  .submit {
    float: right;
  }
}
.comment {
  margin-top: 20px;
  .item {
    margin-top: 20px;
    padding: 10px;
    margin: 0;
    border-top: 1px solid #bfcbd9;
  }
}
.clearfix {
  &:after {
    content: '';
    display: block;
    height: 0;
    clear: both;
    visibility: hidden;
  }
}
.fade-enter-active, .fade-leave-active { transition: opacity .5s; }
.fade-enter, .fade-leave-active { opacity: 0; }
.fade-move { transition: transform .4s; }
.list-enter-active, .list-leave-active { transition: all .5s; }
.list-enter, .list-leave-active { opacity: 0; transform: translateX(30px); }
.list-leave-active { position: absolute !important; }
.list-move { transition: all .5s;}
h4, .content {
  margin-bottom: 20px;
}
.content {
  border: 1px solid #eaeefb;
  padding: 10px;
}
.el-button--success, .header {
  margin-top: 20px;
}
.switch {
  display: inline-block;
  margin-right: 30px;
  height: 42px;
  line-height: 42px;
  vertical-align: baseline;
  margin-bottom: 20px;
}
.document {
  margin-left: 4px;
  color: #c0ccda;
}

.upload {
  display: inline;
  * {
    display: inline;
  }
}
.el-upload-list {
  margin-bottom: 20px;
}
</style>