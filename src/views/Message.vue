<template>
	<section>
		<!--列表-->
		<el-table :data="messages" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" width="55">
			</el-table-column>
			<el-table-column type="index" width="60">
			</el-table-column>
      <el-table-column prop="avatar" width="40">
        <template scope="scope">
          <img :src="scope.row.avatar" class="avatar"/>
        </template>
      </el-table-column> 
			<el-table-column prop="nick_name" label="昵称" width="150" sortable>
			</el-table-column>
			<el-table-column prop="sex" label="性别" width="100" :formatter="formatSex" sortable>
			</el-table-column>
			<el-table-column prop="province" label="省份" width="100" sortable>
			</el-table-column>
			<el-table-column prop="city" label="城市" width="100" sortable>
			</el-table-column>
			<el-table-column prop="signature" label="个性签名" min-width="200" sortable>
			</el-table-column>
			<el-table-column label="操作" width="100">
				<template scope="scope">
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
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

	export default {
		data() {
			return {
				messages: [],
				total: 0,
				page: 1,
				listLoading: false,
				sels: [],//列表选中列
			}
		},
		methods: {
			handleCurrentChange(val) {
				this.page = val;
				this.getMessages();
			},

			getMessages() {
				let para = {
          gid: this.gid || '',
					page: this.page,
					q: this.filters.query,
          type: this.queryType
				};

				this.listLoading = true;
				getMsgList(para).then((res) => {
					this.total = res.data.total;
					this.messages = res.data.messages;
					this.listLoading = false;
				});
			},
			selsChange (sels) {
				this.sels = sels;
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
}
.small-avatar {
    width: 30px;
    height: 30px;
}
.nick-name {
    color: rgb(132, 146, 166);
    font-size: 13px;
    display: inline-block;
    overflow: hidden;
    line-height: 30px;
    height: 30px;
}
</style>