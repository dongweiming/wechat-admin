<template>
	<section>
		<!--列表-->
		<el-table :data="messages" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;" border>
			<el-table-column prop="group" label="群聊" width="160">
        <template scope="scope">
          <div v-if="!isEmptyObject(scope.row.group)">
            <img :src="scope.row.group.avatar" class="avatar"/>
            <a :href="'/#/group/' + scope.row.group.id" class="nick-name">{{scope.row.group.nick_name}}
            </a>
          </div>
        </template>
			</el-table-column>
			<el-table-column prop="sender" label="发送者" width="160">
        <template scope="scope">
          <div v-if="!isEmptyObject(scope.row.sender)">
            <img :src="scope.row.sender.avatar" class="avatar" v-if="scope.row.sender.avatar"/>
            <a href="#" class="nick-name">{{scope.row.sender.nick_name}}</a>
          </div> 
        </template>
			</el-table-column>
			<el-table-column prop="content" label="内容" min-width="200" sortable>
        <template scope="scope">
          <div v-if="scope.row.url">
            <a :href="scope.row.url" target="_blank" class="content">{{scope.row.content}}</a>
          </div>
          <div v-else-if="scope.row.msg_type == 'Picture'">
            <img :src="'/static/img/uploads/' + scope.row.id + scope.row.file_ext" class="picture"/>
          </div>
          <div v-else-if="scope.row.msg_type == 'Video'">
            <video controls="controls" :src="'/static/img/uploads/' + scope.row.id + scope.row.file_ext" class="video"/>
            </video>
          </div>
          <div v-else>{{ scope.row.msg_type == 'Card' ? '名片：' : '' }} {{scope.row.content}}</div>
        </template> 
			</el-table-column>
			<el-table-column prop="date" label="日期" width="180" :formatter="formatTime" sortable>
      </el-table-column>
      <el-table-column prop="msg_type" label="类型" width="100"
        :filters="msgTypeList"
        :filter-method="filterType" filter-placement="bottom-end">
        <template scope="scope">
          <el-tag
            :type="~['Sharing', 'Video', 'Card', 'Picture'].indexOf(scope.row.msg_type) ? 'primary' : 'success'" close-transition>{{getTypeName(scope.row.msg_type)}}</el-tag>
        </template>
      </el-table-column> 
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
			</el-pagination>
		</el-col>
	</section>
</template>

<script>
	import { getMsgList } from '../api/api';
  import { isEmptyObject } from '../common/js/util'

	export default {
		data() {
			return {
				messages: [],
				total: 0,
				page: 1,
				listLoading: false,
				sels: [],//列表选中列
        msgTypeList: [
          { text: 'Card', value: 'Card' },
          { text: '公众号', value: 'MP' },
          { text: '文本', value: 'Text' },
          { text: '视频', value: 'Video' },
          { text: '分享', value: 'Sharing' },
          { text: '图片', value: 'Picture' },
          { text: '默认', value: 'Default' },
        ]
			}
		},
		methods: {
      isEmptyObject( obj ) {
        for ( var name in obj ) {
          return false;
        }
        return true;
      },
      filterType(value, row) {
        return row.msg_type === value;
      },
      getTypeName(text) {
        let rs = '默认';
        this.msgTypeList.forEach((item) => {
          if (item.value == text) {
            rs = item.text
          }
        });
        return rs
      },
			handleCurrentChange(val) {
				this.page = val;
				this.getMessages();
			},

			getMessages() {
				let para = {
					page: this.page,
				};

				this.listLoading = true;
				getMsgList(para).then((res) => {
					this.total = res.data.total;
					this.messages = res.data.messages;
					this.listLoading = false;
				});
			},
			selsChange(sels) {
				this.sels = sels;
			},
      formatTime(row, column) {
        return new Date(row.receive_time).toISOString().slice(0,19).replace(/T/, " ");
      }
		},
		mounted() {
			this.getMessages();
		}
	}

</script>

<style scoped>
.avatar {
    width: 40px;
    height: 40px;
    display: block;
    margin-left: -18px;
    display: inline-block;
}
.content {
    font-size: 14px;
    color: #1f2d3d;
}
.nick-name {
    color: rgb(132, 146, 166);
    font-size: 14px;
    display: inline-block;
    overflow: hidden;
    line-height: 40px;
    text-decoration: none;
    margin-left: 6px;
    white-space: nowrap;
    max-width: 90px;
}
.picture {
  max-height: 120px;
}
.video {
  max-width: 160px;
}
</style>