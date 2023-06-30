"""empty message

<<<<<<< HEAD:migrations/versions/20230628_140637_.py
Revision ID: fa08878de6a3
Revises: 
Create Date: 2023-06-28 14:06:37.825292
=======
Revision ID: 3cb6035758bb
Revises: 
Create Date: 2023-06-28 18:24:15.921305
>>>>>>> dev:migrations/versions/20230628_182415_.py

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
<<<<<<< HEAD:migrations/versions/20230628_140637_.py
revision = 'fa08878de6a3'
=======
revision = '3cb6035758bb'
>>>>>>> dev:migrations/versions/20230628_182415_.py
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasktypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Text(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(length=50), nullable=False),
    sa.Column('lastName', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('isTasker', sa.Boolean(), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tasker_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tasker_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taskertasktypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hourlyRate', sa.Integer(), nullable=True),
    sa.Column('tasker_id', sa.Integer(), nullable=False),
    sa.Column('taskType_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['taskType_id'], ['tasktypes.id'], ),
    sa.ForeignKeyConstraint(['tasker_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('taskTypeId', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('totalPrice', sa.Float(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('task_date', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tasker_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['taskTypeId'], ['tasktypes.id'], ),
    sa.ForeignKeyConstraint(['tasker_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('tasks')
    op.drop_table('taskertasktypes')
    op.drop_table('reviews')
    op.drop_table('users')
    op.drop_table('tasktypes')
    # ### end Alembic commands ###
