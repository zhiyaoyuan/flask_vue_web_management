<template>
  <div class="app-container">
  <div>
    <el-row :gutter="20" justify="space-between">
      <el-col :span="18">
          <h2>设备</h2>
      </el-col>
      <el-col :span="6">
          <el-button size="small" type="primary">创建设备</el-button>
      </el-col>
    </el-row>
  </div>
    <el-table :data="list" v-loading.body="listLoading" element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column label="设备名称" align="center">
        <template slot-scope="scope">
          {{scope.row.username}}
        </template>
      </el-table-column>
      <el-table-column label="设备类型" align="center">
        <template slot-scope="scope">
          <span>{{scope.row.roles}}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
            <el-button size="small" type="primary" plain>查看API-Key和API-Secret</el-button>
          <el-button size="small" type="primary" plain>编辑</el-button>
          <span v-if="'admin'!=scope.row.username">
            <el-button size="small" type="primary" plain>删除</el-button>
          </span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
