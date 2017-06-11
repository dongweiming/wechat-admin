<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.query" placeholder="姓名"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="getUsers">查询</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="handleAdd">添加好友</el-button>
				</el-form-item>
        <el-tag type="primary" style="float: right" v-if="this.group">{{this.group.nick_name}}</el-tag>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
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
			<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
			</el-pagination>
		</el-col>

		<!--新增界面-->
		<el-dialog title="添加好友" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
        <el-form-item label="用户" prop="wxid">
				  <el-select v-model="addForm.wxid" multiple filterable remote placeholder="请输入用户昵称" :remote-method="remoteMethod" size="large">
            <el-option v-for="item in curOptions" :key="item.value" :label="item.label.split('|')[0]" :value="item.value">
              <img :src="item.label.split('|')[1]" class="small-avatar"/>
              <span class="nick-name">{{ item.label.split('|')[0] }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="验证信息" prop="verifyContent">
           <el-input v-model="addForm.verifyContent" auto-complete="off"></el-input>
        </el-form-item>
		  </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="addFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
			</div>
		</el-dialog>
	</section>
</template>

<script>
	import { getUserList, removeUser, addUser, addUsers, batchRemoveUser, getAllUsers } from '../../api/api';

	export default {
		data() {
      var validateForm = (rule, value, callback) => {
          if (value.length == 0) {
              callback(new Error('请至少选择一个用户'));
          } else {
             callback()
          }
      };
			return {
				filters: {
					query: ''
				},
				users: [],
				total: 0,
				page: 1,
        group: '',
				listLoading: false,
				sels: [],//列表选中列

				addFormVisible: false,
				addLoading: false,
				addFormRules: {
					wxid: [
						{ validator: validateForm, trigger: 'blur' }
					]
				},
        curOptions: [],
        allOptions: [],
				addForm: {
					verifyContent: '',
          wxid: ''
				}

			}
		},
    props: ['queryType', 'gid'],
		methods: {
			formatSex: function (row, column) {
				return row.sex == 1 ? '男' : row.sex == 0 ? '女' : '未知';
			},
			handleCurrentChange(val) {
				this.page = val;
				this.getUsers();
			},

			getUsers() {
				let para = {
          gid: this.gid || '',
					page: this.page,
					q: this.filters.query,
          type: this.queryType
				};

				this.listLoading = true;
				getUserList(para).then((res) => {
					this.total = res.data.total;
					this.users = res.data.users;
          this.group = res.data.group;
					this.listLoading = false;
				});
			},

			handleDel: function (index, row) {
				this.$confirm('确认删除该用户吗?', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					let para = { type: this.queryType };
					removeUser(row.id, para).then((res) => {
						this.listLoading = false;
						this.checkStatus(res);
						this.getUsers();
					});
				}).catch(() => {
				});
			},
			handleAdd: function () {
				this.addFormVisible = true;
				this.addForm = {
					verifyContent: '',
          wxid: ''
				};

        getAllUsers().then((res) => {
          this.allOptions = res.data.users.map(item => {
            return { value: item.id, label: `${item.nick_name}|${item.avatar}`};
          });
        });
			},

      remoteMethod(query) {
        if (query !== '') {
          setTimeout(() => {
            this.curOptions = this.allOptions.filter(item => {
              return item.label.split('|')[0].toLowerCase()
                .indexOf(query.toLowerCase()) > -1;
            });
          }, 200);
        } else {
          this.curOptions = [];
        }
      },

			addSubmit: function () {
				this.$refs.addForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.addLoading = true;
							let para = Object.assign({}, this.addForm);
              let func = this.addForm.wxid.length == 1 ? addUser : addUsers;
							func(para).then((res) => {
								this.addLoading = false;
                this.checkStatus(res);
								this.$refs['addForm'].resetFields();
								this.addFormVisible = false;
								this.getUsers();
							});
						});
					}
				});
			},
			selsChange: function (sels) {
				this.sels = sels;
			},

			batchRemove: function () {
				var ids = this.sels.map(item => item.id).toString();
				this.$confirm('确认移除选中用户吗？', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					let para = { ids: ids, type: this.queryType };
					batchRemoveUser(para).then((res) => {
						this.listLoading = false;
						this.checkStatus(res);
						this.getUsers();
					});
				}).catch(() => {

				});
			}
		},
		mounted() {
			this.getUsers();
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